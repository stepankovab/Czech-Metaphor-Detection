import argparse
import torch

from transformers import (
    AutoTokenizer,
    AutoConfig,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    set_seed,
)

import torch.nn.functional as F
from prepare_data import prepare_data
from evaluation_scripts import evaluate_metrics, compute_POS_percentages


parser = argparse.ArgumentParser()
parser.add_argument("--train_languages", nargs="+", default=["cs"], help="Languages to train on")
parser.add_argument("--train_counts", nargs="+", default=[100], help="Number of sentences for each train language")
parser.add_argument("--test_language", default="cs", type=str, help="Test language.")
parser.add_argument("--test_count", default=100, type=int, help="Number of test sentences.")
parser.add_argument("--train_only_pos", nargs="+", default=['VERB'], help="Which pos metaphors to train on.")
parser.add_argument("--test_only_pos", nargs="+", default=['VERB'], help="Which pos metaphors to test on.")
parser.add_argument("--output_dir", default=".", type=str, help="Output directory path.")
parser.add_argument("--source_dir", default=".", type=str, help="Source directory path.")

parser.add_argument("--model_name", default="bert-base-multilingual-cased", type=str, help="Model name in Huggingface Transformers.")
parser.add_argument("--seed", default=42, type=int, help="Seed.")
parser.add_argument("--imbalance_weight", default=0.95, type=float, help="Imbalance weight.")

parser.add_argument("--epochs", default=3, type=int, help="Training epochs.")
parser.add_argument("--train_batch_size", default=32, type=int, help="Train batch size.")
parser.add_argument("--test_batch_size", default=32, type=int, help="Test batch size.")
parser.add_argument("--learning_rate", default=3e-5, type=float, help="Learning rate.")
parser.add_argument("--weight_decay", default=0.01, type=float, help="Weight decay.")
parser.add_argument("--warmup_ratio", default=0.06, type=float, help="Warmup ratio.")

parser.add_argument("--loss", default='focal', type=str, help="focal, weighted")


class WeightedTokenTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**{k: v for k, v in inputs.items() if k != "labels"})
        logits = outputs.logits

        loss_fct = torch.nn.CrossEntropyLoss(
            weight=self.class_weights.to(logits.device) if self.class_weights is not None else None,
            ignore_index=-100
        )
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss


class FocalTokenTrainer(Trainer):
    def __init__(self, *args, gamma=2.0, alpha=None, **kwargs):
        """
        gamma: focusing parameter (>0)
        alpha: weight for classes, tensor of shape [num_labels] or None
        """
        super().__init__(*args, **kwargs)
        self.gamma = gamma
        self.alpha = alpha

    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.get("labels")
        outputs = model(**{k: v for k, v in inputs.items() if k != "labels"})
        logits = outputs.logits  # shape: [batch, seq_len, num_labels]

        # Flatten for token-level
        logits_flat = logits.view(-1, logits.size(-1))
        labels_flat = labels.view(-1)

        # Compute standard CE loss
        ce_loss = F.cross_entropy(
            logits_flat,
            labels_flat,
            reduction="none",
            ignore_index=-100
        )

        pt = torch.exp(-ce_loss)  # pt = probability of the true class
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss

        if self.alpha is not None:
            alpha_factor = self.alpha[labels_flat].to(logits.device)
            focal_loss = alpha_factor * focal_loss

        loss = focal_loss.mean()
        return (loss, outputs) if return_outputs else loss


def main(args):

    print(args)

    set_seed(args.seed)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    train_tokenized, test_tokenized, test_raw = prepare_data(args.train_languages, 
                                                    args.train_counts,
                                                    args.test_language,
                                                    args.test_count,
                                                    args.train_only_pos,
                                                    args.test_only_pos,
                                                    args.source_dir,
                                                    tokenizer)

    print(train_tokenized, test_tokenized)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    config = AutoConfig.from_pretrained(
        args.model_name,
        num_labels=2,
        id2label={0: "NON-MET", 1: "MET"},
        label2id={"NON-MET": 0, "MET": 1},
    )
    model = AutoModelForTokenClassification.from_pretrained(args.model_name, config=config)
    model.to(device)


    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.train_batch_size,
        per_device_eval_batch_size=args.test_batch_size,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        logging_steps=50,              
        logging_dir=f"{args.output_dir}/logs",
        report_to="none",              
        save_total_limit=1,            
        fp16=torch.cuda.is_available(),
        seed=args.seed,
        save_strategy="no",
    )

    
    if args.loss == 'weighted':
        trainer = WeightedTokenTrainer(
            model=model,
            args=training_args,
            train_dataset=train_tokenized,
            eval_dataset=test_tokenized,
            tokenizer=tokenizer,
            compute_metrics=evaluate_metrics,
            class_weights=torch.tensor([1 / (2 * args.imbalance_weight), 1 / (2 * (1 - args.imbalance_weight))], dtype=torch.float),
        )

    
    elif args.loss == 'focal':
        trainer = FocalTokenTrainer(
            model=model,
            args=training_args,
            train_dataset=train_tokenized,
            eval_dataset=test_tokenized,
            tokenizer=tokenizer,
            compute_metrics=evaluate_metrics,
            gamma=2.0
        )

    trainer.train()
    preds, labels, metrics = trainer.predict(test_tokenized)
    print(metrics)

    pos_percentages = compute_POS_percentages(test_raw, preds, labels)
    print(pos_percentages)
    


if __name__ == "__main__":
    main_args = parser.parse_args([] if "__file__" not in globals() else None)
    main(main_args)

