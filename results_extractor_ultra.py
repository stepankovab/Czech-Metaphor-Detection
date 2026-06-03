import ast
from pathlib import Path
from argparse import Namespace
from collections import defaultdict

from tabulate import tabulate


def read_and_parse_entries(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        file_lines = f.readlines()

    entries = []
    current_entry = []
    for line in file_lines:
        if line.startswith("Namespace(") and current_entry != []:
            entries.append(current_entry)
            current_entry = []
        current_entry.append(line[:-1])
    entries.append(current_entry)

    return entries
    

def extract_args(entry):
    for line in entry:
        if line.startswith("Namespace("):
            return eval(line)
        
def extract_train_provided(entry):
    train_data_amount = {}
    train_metaphor_percentage = {}
    for line in entry:
        if line.startswith("train "):
            line_parts = line.split()
            train_data_amount[line_parts[1]] = int(line_parts[5])
            train_metaphor_percentage[line_parts[1]] = round(float(line_parts[6]), 2)

    return train_data_amount, train_metaphor_percentage

def extract_test_provided(entry):
    for line in entry:
        if line.startswith("test "):
            line_parts = line.split()
            return line_parts[1], int(line_parts[5]), round(float(line_parts[6]), 2)
        
def extract_result_dict(entry):
    for line in entry:
        if line.startswith("{'test_loss':"):
            return ast.literal_eval(line)
        
def extract_pos_results(entry: list[str]):
    start_id = None
    for i, line in enumerate(entry):
        if line.startswith("      pos"):
            start_id = i + 1

    pos_results = {}
    if start_id != None:
        for i in range(start_id, len(entry)):
            split_line = entry[i].split()
            if len(split_line) < 7:
                break

            pos_results[split_line[1]] = {'precision': round(float(split_line[5]), 2), 'recall': round(float(split_line[6]), 2), 'f1': round(float(split_line[7]), 2)}

    return pos_results








def read_dicts(data_dir, start_num, end_num, name):
    outputs = []
    train_percentage = None

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

        if content[1 + len(args.train_languages)].startswith("Total train percentage"):
            train_percentage = round(1 - float(content[1 + len(args.train_languages)][len("Total train percentage of metaphor "):]), 3)

        results_dict = ast.literal_eval(content[-5].strip())

        outputs.append((args, results_dict))

    return outputs, train_percentage


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


def gather_by_train_language_train_amount(entries):
    table_dict = {}

    for entry in entries:
        args = extract_args(entry)
        if args.train_languages[0] not in table_dict:
            table_dict[args.train_languages[0]] = {}

        results_dict = extract_result_dict(entry)
        results_dict.update(extract_pos_results(entry))

        amount, _ = extract_train_provided(entry)
        table_dict[args.train_languages[0]][amount[args.train_languages[0]]] = results_dict

    print(args.model_name)
    return table_dict




def gather_by_train_language_permutation(entries):
    table_dict = {}

    for entry in entries:
        args = extract_args(entry)
        if tuple(args.train_languages) not in table_dict:
            table_dict[tuple(args.train_languages)] = {}

        results_dict = extract_result_dict(entry)
        results_dict.update(extract_pos_results(entry))

        table_dict[tuple(args.train_languages)] = results_dict

    print(args.model_name)
    return table_dict

        


def only_relevant_metrics(table_dict):
    new_table_dict = {}

    for key in table_dict.keys():
        new_table_dict[key] = {
            'f1' : table_dict[key]['test_f1'],
            'precision' : table_dict[key]['test_precision'],
            'recall' : table_dict[key]['test_recall'],
            'ADJ_f1' : table_dict[key]['ADJ']['f1'],
            'NOUN_f1' : table_dict[key]['NOUN']['f1'],
            'VERB_f1' : table_dict[key]['VERB']['f1'],
        }
    return new_table_dict



def md_table_lang_order(results):

    rows = []

    for langs, metrics in results.items():
        rows.append([
            ", ".join(langs),   # no arrows
            metrics["f1"],
            metrics["precision"],
            metrics["recall"],
            metrics["ADJ_f1"],
            metrics["NOUN_f1"],
            metrics["VERB_f1"],
        ])

    # Order by F1 descending
    rows = sorted(rows, key=lambda x: x[1], reverse=True)

    # Format numbers
    formatted_rows = [
        [row[0], *[f"{x:.3f}" for x in row[1:]]]
        for row in rows
    ]

    headers = [
        "Languages",
        "F1",
        "Precision",
        "Recall",
        "ADJ F1",
        "NOUN F1",
        "VERB F1",
    ]

    md_table = tabulate(
        formatted_rows,
        headers=headers,
        tablefmt="github"
    )

    print(md_table)



def md_table_data_amount(results):
    
    for lang, lang_results in results.items():

        rows = []

        # Sort by the numeric key (10, 50, 100, ...)
        for n in sorted(lang_results.keys()):
            vals = lang_results[n]

            rows.append([
                n,
                vals["test_precision"],
                vals["test_recall"],
                vals["test_f1"],
                vals["ADJ"]["f1"],
                vals["NOUN"]["f1"],
                vals["VERB"]["f1"],
            ])

        # format floats
        formatted_rows = [
            [row[0], *[f"{x:.3f}" for x in row[1:]]]
            for row in rows
        ]

        headers = [
            "N",
            "Precision",
            "Recall",
            "F1",
            "ADJ F1",
            "NOUN F1",
            "VERB F1",
        ]

        print(f"\n# {lang}\n")

        md_table = tabulate(
            formatted_rows,
            headers=headers,
            tablefmt="github"
        )

        print(md_table)


import matplotlib.pyplot as plt

def plot_language_results(results, lang, outfile):
    lang_results = results[lang]

    # sort by N
    ns = sorted(lang_results.keys())

    accuracy = [lang_results[n]["test_accuracy"] for n in ns]
    precision = [lang_results[n]["test_precision"] for n in ns]
    recall = [lang_results[n]["test_recall"] for n in ns]
    f1 = [lang_results[n]["test_f1"] for n in ns]

    adj_f1 = [lang_results[n]["ADJ"]["f1"] for n in ns]
    noun_f1 = [lang_results[n]["NOUN"]["f1"] for n in ns]
    verb_f1 = [lang_results[n]["VERB"]["f1"] for n in ns]

    plt.figure(figsize=(12, 6))

    plt.plot(ns, accuracy, marker="o", label="Accuracy")
    plt.plot(ns, precision, marker="o", label="Precision")
    plt.plot(ns, recall, marker="o", label="Recall")
    plt.plot(ns, f1, marker="o", label="F1")

    plt.plot(ns, adj_f1, marker="o", linestyle="--", label="ADJ F1")
    plt.plot(ns, noun_f1, marker="o", linestyle="--", label="NOUN F1")
    plt.plot(ns, verb_f1, marker="o", linestyle="--", label="VERB F1")

    plt.xlabel("N")
    plt.ylabel("Score")
    plt.title(f"Metrics for {lang}")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(outfile, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    # file_name = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/out_large_scale/Monolingual_data_amount_mm.o20772848"
    # file_name = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/out_large_scale/Monolingual_data_amount.o20772810"
    # file_name = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/out_large_scale/unannotated_data_amount_mm.o20810683"
    file_name = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/out_large_scale/Multilingual_data_amount_2_mm.o20772847"
    # file_name = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/out_large_scale/Multilingual_data_amount_2.o20772811"
    # file_name = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/out_large_scale/language_permutations.o20772805"

    entries = read_and_parse_entries(file_name)
    
    a = gather_by_train_language_train_amount(entries)
    # a = gather_by_train_language_permutation(entries)
    # b = only_relevant_metrics(a)

    # md_table_lang_order(b)

    # md_table_data_amount(a)
    # plot_language_results(a, "cs_unannotated", "fig_cs_unannotated")
    plot_language_results(a, "es", "fig_es_multilingual")




    # relevant_args = ["imbalance_weight"]

    # outputs, train_percentage = read_dicts(data_dir, start_num, end_num, name)
    # tabulated_dict = extract_metrics(outputs, relevant_args)
    # markdown_table = generate_markdown_table(tabulated_dict, relevant_args)

    # print(generate_language_count_header(args=outputs[0][0]))
    # print()
    # print(f"Train imbalance = `{train_percentage}`")
    # print()
    # print(markdown_table)
