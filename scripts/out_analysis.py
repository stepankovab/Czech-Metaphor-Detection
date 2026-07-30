import json
import os
import pandas as pd

# with open("out/841ec20e-ec1b-4fee-b96c-c3c4384bec9c.json", 'r', encoding='utf-8') as f: # all 4 to cs f1 0.69 
# with open("out_cs_poetry/ec468f5f-4a99-4410-b7c4-26edaa3e4322.json", 'r', encoding='utf-8') as f:  # cs poetry
# with open("out/b4039236-b58a-4161-ada2-e1cf7f2d0466.json", 'r', encoding='utf-8') as f:  # cs
# with open("out/6176f0a0-0add-491d-9c0e-8a7cf122cc12.json", 'r', encoding='utf-8') as f:  # sl
# with open("out/5f14ded9-cd76-4b76-a3eb-7fad8b5da302.json", 'r', encoding='utf-8') as f:  # en
# with open("out/857ab3da-a7c1-48e4-a25c-57fda0b1ec9f.json", 'r', encoding='utf-8') as f:  # en translated from cs

    # results = dict(json.load(f))

folder = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/outputs/out_sl90_words"

results_list = []
for filename in os.listdir(folder):
    if filename.endswith(".json"):
        with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
            results_list.append(json.load(f))

results_list.sort(
    key=lambda d: tuple(d["words"][str(i)] for i in range(min(5, len(d["words"]))))
)

# dict_keys(['words', 'poss', 'preds', 'labels'])


# with open("model_annotated_cs.txt", 'w', encoding='utf-8') as f:

# # for results in results_list:
# for i in range(len(results["words"])):
#     note = ""
#     if results["preds"][str(i)] == 1:
#         if results['labels'][str(i)] == 1:
#             note = "   ---   poznal"

#         if  results['labels'][str(i)] == 0:
#             note = "   ---   navic"

#     if results["preds"][str(i)] == 0:
#         if results['labels'][str(i)] == 1:
#             note = "   ---   miss"

# # f.write(results["words"][str(i)] + " " + note + "\n")
#     print(results["words"][str(i)], note)




# with open("cs_extras.txt", "w", encoding="utf-8") as f:
#     for results in results_list:
#         for i in range(len(results["words"])):
#             note = ""
#             if results["preds"][str(i)] == 1:
#                 if  results['labels'][str(i)] == 0:
#                     interesting_part = [results["words"][str(min(j, len(results["words"])-1))] for j in range(i-4,i+4)]
#                     interesting_part.insert(5, ']')
#                     interesting_part.insert(4, '[')
#                     print(" ".join(interesting_part))
#                     f.write(" ".join(interesting_part) + "\n")



dfs = []

for results in results_list:
    df = pd.DataFrame(results)
    # print(df.head(10))
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)
# combined_df.to_csv(f"{folder}/{folder}_concat_results.csv", index=False)


# from sklearn.metrics import precision_score, recall_score, f1_score


# def _compute_scores(df):
#     """Precision / Recall / F1 for a dataframe."""

#     return {
#         "precision": precision_score(
#             df["labels"], df["preds"], zero_division=0
#         ),
#         "recall": recall_score(
#             df["labels"], df["preds"], zero_division=0
#         ),
#         "f1": f1_score(
#             df["labels"], df["preds"], zero_division=0
#         ),
#         "n": len(df)
#     }


def metaphor_report(df):

    report = {}

    # ############################################################
    # # Overall
    # ############################################################

    # report["overall"] = pd.DataFrame([_compute_scores(df)])

    # ############################################################
    # # NOUN + VERB + ADJ together
    # ############################################################

    pos_df = df[df["poss"].isin(["NOUN", "VERB", "ADJ"])]


    # report["noun_verb_adj"] = pd.DataFrame([_compute_scores(pos_df)])

    ############################################################
    # Individual POS
    ############################################################

    # rows = []

    # for pos in ["NOUN", "VERB", "ADJ"]:

    #     tmp = pos_df[pos_df["poss"] == pos]

    #     scores = _compute_scores(tmp)
    #     scores["POS"] = pos

    #     rows.append(scores)

    # report["per_pos"] = (
    #     pd.DataFrame(rows)
    #     .set_index("POS")
    # )

    ############################################################
    # TP / FP / FN analysis
    ############################################################

    pos_df = pos_df.copy()

    pos_df["case"] = None

    pos_df.loc[
        (pos_df.labels == 1) & (pos_df.preds == 1),
        "case"
    ] = "TP"

    pos_df.loc[
        (pos_df.labels == 0) & (pos_df.preds == 1),
        "case"
    ] = "FP"

    pos_df.loc[
        (pos_df.labels == 1) & (pos_df.preds == 0),
        "case"
    ] = "FN"


    analysis = (
        pos_df[pos_df["case"].notna()]
        .groupby(["case", "direct_en_translation", "type_label"])
        .size()
        .unstack(fill_value=0)
    )


    report["tp_fp_fn"] = analysis

    ############################################################
    # Pretty version
    ############################################################

    pretty = []

    for case in ["TP", "FP", "FN"]:

        tmp = pos_df[pos_df.case == case]

        row = {"case": case}

        for label in [0, 1]:
            for t in ["c", "n", "x"]:

                row[f"{label}-{t}"] = (
                    (
                        (tmp.direct_en_translation == label)
                        &
                        (tmp.type_label == t)
                    ).sum()
                )

        pretty.append(row)

    report["tp_fp_fn_pretty"] = (
        pd.DataFrame(pretty)
        .set_index("case")
    )

    return report



df_annotations = pd.read_csv("/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/annotated_novel_translations.csv")[["direct_en_translation", "type_label"]]
combined_df["direct_en_translation"] = df_annotations["direct_en_translation"]
combined_df["type_label"] = df_annotations["type_label"]

report = metaphor_report(df=combined_df)



# for _, row in combined_df.iterrows():
#     if row.labels == 0 and row.preds == 1 and row.direct_en_translation in [0,1]:
#         print(row)



print(report["tp_fp_fn_pretty"])



# Na vsech datech + cs
#       0-c  0-n  0-x  1-c  1-n  1-x
# case                              
# TP     30    5    0   49    3    2
# FP      3    0    0    3    0    0
# FN     76    7    3   22   17   21

# na 30k en, 30k es, 30k sl + cs
#       0-c  0-n  0-x  1-c  1-n  1-x
# case                              
# TP     34    4    0   41    1    3
# FP      3    0    0    3    0    0
# FN     72    8    3   30   19   20

# jen na anglictine 90k + cs 
#       0-c  0-n  0-x  1-c  1-n  1-x
# case                              
# TP     32    7    1   37    3    5
# FP      2    0    0    2    0    0
# FN     74    5    2   34   17   18

# jen na sl 90k + cs
#       0-c  0-n  0-x  1-c  1-n  1-x
# case                              
# TP     19    2    0   38    3    1
# FP      3    0    0    3    0    0
# FN     87   10    3   33   17   22



# jen na anglictine 90k no cs
#       0-c  0-n  0-x  1-c  1-n  1-x
# case                              
# TP     15    1    0   22    2    1
# FP      0    0    0    1    0    0
# FN     91   11    3   49   18   22


# na vsem 30k + 30k + 30k BEZ cs 
#       0-c  0-n  0-x  1-c  1-n  1-x
# case                              
# TP     11    1    0   16    1    0
# FP      1    0    0    0    0    0
# FN     95   11    3   55   19   23


