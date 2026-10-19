# Czech Metaphor Detection

Research code and processed datasets for token-level metaphor detection in Czech, using MIPVU annotations and multilingual transformer models.

## Data

| Dataset | Words | Sentences | Metaphors |
| --- | ---: | ---: | ---: |
| English (VUA) | 237,247 | 16,202 | 10.9% |
| Spanish (CoMeta) | 116,976 | 3,631 | 1.8% |
| Slovenian (Komet) | 259,881 | 13,963 | 6.22% |
| Czech general | 4,659 | 236 | 10.5% |
| Czech poetry | 685 | 43 | 17.2% |

## Experiments

We compare cross-lingual training from English, Spanish, and Slovenian with training that also includes Czech annotations. Multilingual training experiments use about 94,000 words (just under 4,000 Czech words) and five-fold evaluation on Czech data.

The results show that multilingual transfer helps Czech metaphor detection, and even a small amount of Czech training data substantially improves it.

Datasets are in `Data/`. Training and evaluation code is in `Experiments/model_training/`, preprocessing and analysis scripts are in `Data/` and `Experiments/Data_analysis/`.
