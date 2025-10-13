from load_SLO import load_komet
from load_VUE import load_vuamc
from load_SPA_cometa import load_cometa_words

import matplotlib.pyplot as plt


LANG = 'Spanish'

if LANG == 'Slovenian':
    XML_FILE_PATH = './Data/Komet_Slovenian/komet.tei/komet.xml'
    df = load_komet(XML_FILE_PATH, None, None)
elif LANG == 'English':
    VUE_FILE_PATH = './Data/VUA/VUAMC.xml'
    df = load_vuamc(VUE_FILE_PATH, None, None)
elif LANG == 'Spanish':
    COMETA_FILE_PATH = './Data\cometa_dataset_v1\cometa_pos_train.tsv'
    df = load_cometa_words(COMETA_FILE_PATH, None, None)

# print(df)

# print(df.where(df['labels']).dropna()['pos'])

# bins_vals = list(set(df['pos']))
# bins = len(bins_vals)

# print(bins)


# plt.title(f"Number of metaphors in {LANG}")
# plt.hist(df["pos"], bins=bins)
# plt.hist(df.where(df['labels']).dropna()['pos'], color="orange", bins=bins)
# # plt.hist(df.where(~df['labels']).dropna()['pos'], color="red", bins=bins)
# plt.xticks(rotation=45)
# plt.show()



# values_of_pos = []

# for bin in bins_vals:

#     temp_df = df.where(df["pos"] == bin).dropna()
#     temp_df_met = temp_df.where(df["labels"]).dropna()


#     values_of_pos.append((bin, len(temp_df), len(temp_df_met), round(len(temp_df_met) / len(temp_df), 3)))

# values_of_pos.sort(key = lambda x : x[3])

# for tup in values_of_pos:
#     print(tup)



print(len(df.where(df['labels']).dropna()['pos']) / len(df))


