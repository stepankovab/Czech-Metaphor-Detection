from transformers import AutoTokenizer, AutoModel
import torch
import json
import itertools



with open("out/841ec20e-ec1b-4fee-b96c-c3c4384bec9c.json", 'r', encoding='utf-8') as f:
    cs_data = json.load(f)


with open("out/857ab3da-a7c1-48e4-a25c-57fda0b1ec9f.json", 'r', encoding='utf-8') as f:
    en_data = json.load(f)




MODEL_NAME = "bert-base-multilingual-cased"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# model.eval()

sent_src = list(cs_data['words'].values())
sent_tgt = list(en_data['words'].values())



# pre-processing
token_src, token_tgt = [tokenizer.tokenize(word) for word in sent_src], [tokenizer.tokenize(word) for word in sent_tgt]
wid_src, wid_tgt = [tokenizer.convert_tokens_to_ids(x) for x in token_src], [tokenizer.convert_tokens_to_ids(x) for x in token_tgt]
ids_src, ids_tgt = tokenizer.prepare_for_model(list(itertools.chain(*wid_src)), return_tensors='pt', model_max_length=tokenizer.model_max_length, truncation=True)['input_ids'], tokenizer.prepare_for_model(list(itertools.chain(*wid_tgt)), return_tensors='pt', truncation=True, model_max_length=tokenizer.model_max_length)['input_ids']
sub2word_map_src = []
for i, word_list in enumerate(token_src):
  sub2word_map_src += [i for x in word_list]
sub2word_map_tgt = []
for i, word_list in enumerate(token_tgt):
  sub2word_map_tgt += [i for x in word_list]

# alignment
align_layer = 8
threshold = 1e-3
model.eval()
with torch.no_grad():
  out_src = model(ids_src.unsqueeze(0), output_hidden_states=True)[2][align_layer][0, 1:-1]
  out_tgt = model(ids_tgt.unsqueeze(0), output_hidden_states=True)[2][align_layer][0, 1:-1]

  dot_prod = torch.matmul(out_src, out_tgt.transpose(-1, -2))

  softmax_srctgt = torch.nn.Softmax(dim=-1)(dot_prod)
  softmax_tgtsrc = torch.nn.Softmax(dim=-2)(dot_prod)

  softmax_inter = (softmax_srctgt > threshold)*(softmax_tgtsrc > threshold)

align_subwords = torch.nonzero(softmax_inter, as_tuple=False)
align_words = set()
for i, j in align_subwords:
  align_words.add( (sub2word_map_src[i], sub2word_map_tgt[j]) )


cs_labels = list(cs_data['labels'].values())
cs_preds = list(cs_data['preds'].values())
en_preds = list(en_data['preds'].values())


aligned_labels = {'cs_labels': [],
                  'cs_preds': [],
                  'en_preds': [],
                  'preds_combined': []}

aligned_words = []

for i, j in sorted(align_words):
   aligned_labels['cs_labels'].append(cs_labels[i])
   aligned_labels['cs_preds'].append(cs_preds[i])
   aligned_labels['en_preds'].append(en_preds[j])
   aligned_labels['preds_combined'].append(int(cs_preds[i] or en_preds[j]))
   aligned_words.append(sent_src[i])



print(len(aligned_labels['cs_labels']), len(aligned_labels['en_preds']))



from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

def compute_metrics(y_true, y_pred):
    print("Precision:", precision_score(y_true, y_pred))
    print("Recall:", recall_score(y_true, y_pred))
    print("F1:", f1_score(y_true, y_pred))
    print()

    # print(classification_report(y_true, y_pred))

compute_metrics(aligned_labels['cs_labels'], aligned_labels['cs_preds'])
compute_metrics(aligned_labels['cs_labels'], aligned_labels['en_preds'])
compute_metrics(aligned_labels['cs_preds'], aligned_labels['en_preds'])
compute_metrics(aligned_labels['cs_labels'], aligned_labels['preds_combined'])



for word, label in zip(aligned_words, aligned_labels['preds_combined']):
    note = ""
    if label == 1:
      note = "    --- met"
    print(word, note)
    