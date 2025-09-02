# # # import xml.etree.ElementTree as ET
# # # import pandas as pd

# # # # def load_vuamc_words(vuamc_xml_path: str, elements=-1) -> pd.DataFrame:
# # # #     """
# # # #     Parse VU Amsterdam Metaphor Corpus (TEI P5) and return a DataFrame with:
# # # #     columns: ['word', 'metaphor'] where 'metaphor' is bool.
# # # #     Includes punctuation and preserves the original token order.
# # # #     """
# # # #     ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
# # # #     tree = ET.parse(vuamc_xml_path)
# # # #     root = tree.getroot()

# # # #     tokens = []
# # # #     labels = []

# # # #     # Iterate over all sentences
# # # #     for s in root.findall('.//tei:s', ns):
# # # #         for child in s:
# # # #             if child.tag == f"{{{ns['tei']}}}w":  # word element
# # # #                 token_text = (child.text or '').strip()
# # # #                 is_met = False
# # # #                 seg = child.find('tei:seg', ns)
# # # #                 if seg is not None and (seg.get('type') == 'met' or seg.get('function') == 'mrw'):
# # # #                     inner_text = (seg.text or '').strip()
# # # #                     if inner_text:
# # # #                         token_text = inner_text
# # # #                     is_met = True
# # # #                 if token_text:
# # # #                     tokens.append(token_text)
# # # #                     labels.append(is_met)
# # # #             elif child.tag == f"{{{ns['tei']}}}c":  # punctuation element
# # # #                 token_text = (child.text or '').strip()
# # # #                 if token_text:
# # # #                     tokens.append(token_text)
# # # #                     labels.append(False)

# # # #     df = pd.DataFrame({'word': tokens[:elements], 'metaphor': labels[:elements]})
# # # #     return df




# # # # df = load_vuamc_words("Data/VUA/VUAMC.xml", 2324567890)



# # # # print(len(df[:1000]))

# # # # print(df[10000:11000])




# # # def load_czech(czech_path) -> pd.DataFrame:
# # #     df = pd.read_csv(czech_path, header=None)
# # #     df = df.T
# # #     df.columns = ['word', 'metaphor']
# # #     df['metaphor'] = df['metaphor'].astype(int).astype(bool)

# # #     new_words = []
# # #     new_labels = []

# # #     for word, label in zip(df['word'], df['metaphor']):
# # #         if len(word) <= 1:
# # #             new_words.append(word)
# # #             new_labels.append(label)
# # #             continue

# # #         if word[-1].isalpha():
# # #             new_words.append(word)
# # #             new_labels.append(label)
# # #             continue

# # #         new_words.append(word[:-1])
# # #         new_labels.append(label)
# # #         new_words.append(word[-1])
# # #         new_labels.append(False)

# # #     return pd.DataFrame({'word': new_words, 'metaphor': new_labels})


# # # print(load_czech("Data/CZECH_Dalibor/pokus_train_data.csv"))







# # import os
# # import pandas as pd

# # # Input folder with your XLSX files
# # input_folder = "Data\CZECH_Dalibor\Metaphor Annotation Data"
# # # Output folder where CSVs will be saved
# # output_folder = "Data\CZECH_Dalibor\Metaphor_csvs"
# # os.makedirs(output_folder, exist_ok=True)

# # for filename in os.listdir(input_folder):
# #     if filename.endswith(".xlsx"):
# #         filepath = os.path.join(input_folder, filename)
# #         # Load workbook with all sheets
# #         xls = pd.ExcelFile(filepath)
        
# #         for sheet_name in xls.sheet_names:
# #             # Read each sheet into a DataFrame
# #             df = pd.read_excel(filepath, sheet_name=sheet_name)
            
# #             # Create a CSV name: <originalfilename>_<sheetname>.csv
# #             base = os.path.splitext(filename)[0]
# #             safe_sheet = sheet_name.replace(" ", "_").replace("/", "-")
# #             csv_name = f"{base}_{safe_sheet}.csv"
# #             csv_path = os.path.join(output_folder, csv_name)
            
# #             # Save as CSV
# #             df.to_csv(csv_path, index=False, encoding="utf-8")
# #             print(f"Saved {csv_path}")




# # import os
# # import pandas as pd

# # input_folder = "Data\CZECH_Dalibor\Metaphor_csvs"
# # output_folder = "Data\CZECH_Dalibor\Metaphor_cleaned_csv"
# # os.makedirs(output_folder, exist_ok=True)


# # for filename in os.listdir(input_folder):
# #     if not filename.endswith(".csv"):
# #         continue

# #     filepath = os.path.join(input_folder, filename)

# #     # Read file without header so nothing becomes "Unnamed"
# #     df = pd.read_csv(filepath, header=None)

# #     # Drop rows that are completely empty
# #     df = df.dropna(how="all")

# #     # Drop rows where every cell starts with "Unnamed"
# #     df = df[~df.apply(lambda row: all(str(x).startswith("Unnamed") for x in row if pd.notna(x)), axis=1)]

# #     if df.empty:
# #         continue

# #     # First non-empty row = words
# #     words = df.iloc[0].tolist()

# #     # Remaining rows = annotations
# #     annotations = df.iloc[1:]
# #     annotations = annotations.dropna(how="all")

# #     # Build clean dataframe
# #     clean_df = pd.DataFrame({"word": words})

# #     # Add annotations as columns (ann1, ann2, ...)
# #     for i, row in enumerate(annotations.values):
# #         clean_df[f"ann{i+1}"] = row

# #     # Save cleaned CSV
# #     outpath = os.path.join(output_folder, filename)
# #     clean_df.to_csv(outpath, index=False, encoding="utf-8")
# #     print(f"Saved cleaned file: {outpath}")


# # import os
# # import pandas as pd
# # from collections import defaultdict

# # input_folder = "Data\CZECH_Dalibor\Metaphor_cleaned_csv"

# # # Dictionary: key = tuple of words, value = list of filenames that contain it
# # word_sequences = defaultdict(list)

# # for filename in os.listdir(input_folder):
# #     if not filename.endswith(".csv"):
# #         continue

# #     filepath = os.path.join(input_folder, filename)
# #     df = pd.read_csv(filepath)

# #     if "word" not in df.columns:
# #         continue

# #     # Convert the word column into a tuple (immutable, usable as dict key)
# #     words_tuple = tuple(df["word"].dropna().tolist())

# #     # Store mapping
# #     word_sequences[words_tuple].append(filename)

# # # Report duplicates
# # for words_tuple, files in word_sequences.items():
# #     if len(files) > 1:
# #         print("Duplicate sequence found in:")
# #         for f in files:
# #             print(f"  - {f}")
# #         print("-" * 40)


# # import os
# # import shutil
# # import pandas as pd
# # from collections import defaultdict

# # input_folder = r"Data\CZECH_Dalibor\Metaphor_cleaned_csv"
# # output_folder = r"Data\CZECH_Dalibor\Grouped"

# # # Create output base folders
# # duplicates_folder = os.path.join(output_folder, "duplicates")
# # unique_folder = os.path.join(output_folder, "unique")
# # os.makedirs(duplicates_folder, exist_ok=True)
# # os.makedirs(unique_folder, exist_ok=True)

# # # Dictionary: key = tuple of words, value = list of filenames that contain it
# # word_sequences = defaultdict(list)

# # # Step 1: Scan all CSVs and collect word sequences
# # for filename in os.listdir(input_folder):
# #     if not filename.endswith(".csv"):
# #         continue

# #     filepath = os.path.join(input_folder, filename)
# #     df = pd.read_csv(filepath)

# #     if "word" not in df.columns:
# #         continue

# #     # Convert the word column into a tuple (immutable, usable as dict key)
# #     words_tuple = tuple(df["word"].dropna().tolist())

# #     # Store mapping
# #     word_sequences[words_tuple].append(filename)

# # # Step 2: Group files into folders
# # group_counter = 1
# # for words_tuple, files in word_sequences.items():
# #     if len(files) > 1:
# #         # Make a folder for this duplicate group
# #         group_path = os.path.join(duplicates_folder, f"group_{group_counter}")
# #         os.makedirs(group_path, exist_ok=True)
# #         for f in files:
# #             shutil.copy(os.path.join(input_folder, f), os.path.join(group_path, f))
# #         group_counter += 1
# #     else:
# #         # Unique file → send to "unique" folder
# #         f = files[0]
# #         shutil.copy(os.path.join(input_folder, f), os.path.join(unique_folder, f))

# # print("✅ Grouping finished!")
# # print(f"Duplicates grouped into: {duplicates_folder}")
# # print(f"Uniques moved into: {unique_folder}")

# import os
# import pandas as pd

# duplicates_folder = r"Data\CZECH_Dalibor\Grouped\duplicates"

# # Go through each group folder
# for group_name in os.listdir(duplicates_folder):
#     group_path = os.path.join(duplicates_folder, group_name)
#     if not os.path.isdir(group_path):
#         continue

#     csv_files = [f for f in os.listdir(group_path) if f.endswith(".csv")]
#     dfs = []

#     # Load all CSVs in the group
#     for f in csv_files:
#         df = pd.read_csv(os.path.join(group_path, f))
#         dfs.append(df)

#     if not dfs:
#         continue

#     # Step 1: Collect all annotation columns from all files
#     all_columns = set()
#     for df in dfs:
#         # Only include columns without missing values
#         valid_cols = [col for col in df.columns if df[col].notna().all()]
#         all_columns.update(valid_cols)

#     # Step 2: Deduplicate columns by content
#     merged_df = pd.DataFrame()
#     seen_contents = set()

#     for df in dfs:
#         for col in all_columns:
#             if col in df.columns:
#                 col_values = tuple(df[col].tolist())
#                 if col_values not in seen_contents:
#                     merged_df[col] = df[col]
#                     seen_contents.add(col_values)

#     # Save merged CSV inside the group folder
#     output_path = os.path.join(group_path, f"{group_name}_merged.csv")
#     merged_df.to_csv(output_path, index=False)
#     print(f"Saved merged CSV in group folder: {output_path}")

# print("✅ All groups merged successfully!")


import pandas as pd

# Path to your merged CSV
input_csv = r"Data/CZECH_Dalibor/final/group_3_merged.csv"
output_csv = r"Data/CZECH_Dalibor/group_3_merged.csv"

# Load
df = pd.read_csv(input_csv)

# Take only word + ann1
if 'ann1' not in df.columns:
    raise ValueError("No ann1 column found in the CSV!")

# Create new DataFrame with words as columns, ann1 as one row
pivot_df = pd.DataFrame([df['ann1'].tolist()], columns=df['word'].tolist())

# Save
pivot_df.to_csv(output_csv, index=False)

print(f"✅ Saved pivoted CSV: {output_csv}")
