# Data Collection

## Metaphor Detection

### Tsvetkov

From paper *Metaphor Detection with Cross-Lingual Model Transfer*

- SVO dataset created from TroFi
    - Each sentence contains either literal or metaphorical use for one of 50 English verbs. First, we use a dependency parser to extract subject-verb-object (SVO) relations. Then, we filter extracted relations to eliminate parsing-related errors, and relations with verbs which are not in the TroFi verb list. After filtering, there are 953 metaphorical and 656 literal SVO relations which we use as a training set.

- AN in `Data\Tsvestkov`
    - training set containing 884 metaphorical AN pairs and 884 pairs with literal meaning. It was collected by two annotators using public resources (collections of metaphors on the web). At least one additional person carefully examined and culled the collected metaphors, by removing duplicates, weak metaphors, and metaphorical phrases (such as drowning students) whose interpretation depends on the context.


### Kesarwani

From paper *Metaphor Detection in a Poetry Corpus*

- https://www.eecs.uottawa.ca/~diana/resources/metaphor/
    - "Coming soon"

- Details in the paper in section *Annotating the Corpus*
- Basically N-V-N metaphores anotated as either metaphor or not, with marked head of a sentence


### VUA

VU Amsterdam Metaphor Corpus (VUA)
- There are altogether 117 texts covering four genres (academic, conversation, fiction, news)

https://github.com/EducationalTestingService/metaphor/tree/master/VUA-shared-task
- detailed descriotion on how to parse the xml file
- each word is either 0 (not a metaphor) or 1 (MRW)
    - *Each word, including function words, is annotated as metaphoric or literal*
    - *including the non-spatial meaning of in* [*An analysis of language models for metaphor recognition*]


When downloading from the most spread link: https://ota.ahds.ac.uk/headers/2541.xml I get 404 error. However I think I got the file anyway at `Data\VUA_shared_task\2541.xml`


What is `VUA-ALL-POS` and `VUA-SEQ` ???
- [*An analysis of language models for metaphor recognition*] vyhodnocuje na jednotlivych ?verzich? VUA 

### TOEFL essays

This repository contains 180 (train) / 60 (test) essays [https://aclanthology.org/N18-2014/]

- Need to ask for permission to use
- https://catalog.ldc.upenn.edu/LDC2014T06
- Used in the 2020 shared task on metaphor detection
    - https://github.com/EducationalTestingService/metaphor/tree/master/TOEFL-release

```
As people M_climb M_the M_ladder of success their ideas tend to change from M_dynamic and innovative to M_static and conservative .
I believe that succesful poeple M_focus and doing what they already know how to do rather than M_exploring or trying out new things and taking risks .
M_Reaching a M_level of success whether in bussiness or in life M_requires time and hard work , and upon M_reaching success risk would be to huge of a M_price .
```


**For both VUA and TOEFL there is a github release page: maybe download from there?**
- https://github.com/EducationalTestingService/metaphor/releases/tag/v1.0
    - password protected


### MOH-X

Mohammad et al 2016
- verb metaphor detection database with the data from WordNet
- emotions are there

### TroFi

- verb metaphor detection dataset consisting of sentences from the 1987-89 Wall Street Journal Corpus Release 1


### LCC - English, Spanish, Russian, Farsi

- big
- anotating pairs of words
- [TODO] stahnout


### KOMET - Slovenian

The dataset is difficult to use from a machine-learning perspective, because it has a very broad definition of metaphorical language, and many noisy examples. In terms of metaphor types, the corpus contains direct and indirect metaphors1, edge-case metaphors which can be interpreted literally or metaphorically depending on the wider (extra-textual) context, and metaphoric signifier information which denotes so called “metaphor flags” - expressions that indicate metaphorical use (such as “like” or “metaphorically speaking”). For a large number of metaphors, no type is specified. [*Extracting and Analysing Metaphors in Migration Media Discourse: towards a Metaphor Annotation Scheme*]

- 200k words
- MIPVU


### CoMeta - Spanish

- big spanish MIPVU anotated dataset


## Metaphor Paraphrasing

### Bizzoni

https://github.com/yuri-bizzoni/Metaphor-Paraphrase

- One metaphorical sentence and 4 paraphrases with various degree of correctness


### Vita

it is a task to decide whether a given English sentence containing a metaphor convey or not convey the same (or almost the same) meaning as a given Czech sentence with no metaphorical expressions.

- the first sentence in English contains a metaphorical expression, the second sentence, in Czech, is a potential paraphrase candidate followed by its translation to English

- https://github.com/martinvita/FigurativeLanguageParaphrasing/blob/master/crossLingualMetaphorParaphraseEN-CZ.csv