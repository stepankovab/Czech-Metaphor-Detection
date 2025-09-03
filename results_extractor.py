import ast
from pathlib import Path
from argparse import Namespace
from collections import defaultdict


def read_dicts(data_dir, start_num, end_num, name):
    outputs = []

    for file_path in Path(data_dir).iterdir():
        file_path = str(file_path)
        file_num = int(file_path[-8:])
        if file_num < start_num or file_num > end_num:
            continue

        if file_path[(-10 - len(name)):-10] != name:
            continue
        
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()

        namespace_string = content[0].strip()
        if namespace_string.startswith("Namespace(train_languages=['"):
            args = eval(namespace_string)
        else:
            raise Exception()

        results_idx = 10 + len(args.train_languages)
        if content[3].startswith("Total train percentage"):
            results_idx += 1

        results_dict = ast.literal_eval(content[results_idx].strip())

        outputs.append((args, results_dict))

    return outputs


def extract_metrics(outputs, relevant_args: list):
    stratified_metrics = defaultdict(dict)
    
    for args, results_dict in outputs:
        key = tuple(getattr(args, arg) for arg in relevant_args)
        
        metrics = {
            'precision': results_dict.get('eval_precision'),
            'recall': results_dict.get('eval_recall'),
            'f1': results_dict.get('eval_f1'),
            'accuracy': results_dict.get('eval_accuracy')
        }
        stratified_metrics[key] = metrics
        
    sorted_metrics = dict(sorted(stratified_metrics.items()))

    return sorted_metrics


def generate_markdown_table(data_dict, relevant_args):
    metric_names = list(next(iter(data_dict.values())).keys())
    headers = relevant_args + metric_names
    header_line = "| " + " | ".join(headers) + " |"
    
    separator_line = "| " + " | ".join(['---'] * len(headers)) + " |"
    
    rows = []
    for key, metrics in data_dict.items():
        key_tuple = key if isinstance(key, tuple) else (key,)
        row_values = list(key_tuple) + [f"{metrics[m]:.4f}" for m in metric_names]
        rows.append("| " + " | ".join(map(str, row_values)) + " |")

    table_lines = [header_line, separator_line] + rows
    return "\n".join(table_lines)


def generate_language_count_header(args):
    train_parts = [
        f"{lang.upper()}({count})"
        for lang, count in zip(args.train_languages, args.train_counts)
    ]
    train_string = " ".join(train_parts)
    test_string = f"{args.test_language.upper()}({args.test_count})"
    heading = f"### {train_string} - {test_string}"
    
    return heading








data_dir = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/out"

start_num = 12767212
end_num   = 12799999

name = "EN10000CSc-CS"

relevant_args = ["imbalance_weight"]

outputs = read_dicts(data_dir, start_num, end_num, name)
tabulated_dict = extract_metrics(outputs, relevant_args)
markdown_table = generate_markdown_table(tabulated_dict, relevant_args)

print(generate_language_count_header(args=outputs[0][0]))
print(markdown_table)
