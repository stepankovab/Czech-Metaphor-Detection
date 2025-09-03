# Primary results

In these results, there are mistakes like leakage of train-test data with the Czech dataset, or unlabeled Slovenian, marked as `EMPTY DATASET`.

## EN

### to EN (2k words)

| Train | Precision | Recall | F1     | Accuracy |
|-------|-----------|--------|--------|----------|
| None  | 0.1385    | 0.6962 | 0.2310 | 0.3975   |
|CS 1.4k| 0.2255    | 0.3269 | 0.2669 | 0.7665   |
| 10k   | 0.5478    | 0.8763 | 0.6743 | 0.8425   |
| 100k  | 0.0       | 0.0    | 0.0    | 0.944    |


### to CS (1414 words)

| Train | Precision | Recall | F1     | Accuracy |
|-------|-----------|--------|--------|----------|
| 1k    | 0.1757    | 0.6    | 0.2718 | 0.6818   |
| 2k    | 0.1576    | 0.7643 | 0.2613 | 0.5721   |
| 10k   | 0.2516    | 0.5643 | 0.348  | 0.7907   |
| 100k  | 0.2788    | 0.5357 | 0.3667 | 0.8168   |


## EN + CS (703 words)

### to CS (1414 words)

| Train | Precision | Recall | F1     | Accuracy |
|-------|-----------|--------|--------|----------|
| 2k    | 0.2139    | 0.7929 | 0.3369 | 0.6909   |
| 10k   | 0.2478    | 0.8071 | 0.3792 | 0.7383   |
| 100k  | 0.2916    | 0.8143 | 0.4294 | 0.7857   |


## SL

### to SL (2k words)

| Train | Precision | Recall | F1  | Accuracy |
|-------|-----------|--------|-----|----------|
| A     | 0.0       | 0.0    | 0.0 | 0.0      |


### to CS (1414 words)

| Train | Precision | Recall | F1  | Accuracy |
|-------|-----------|--------|-----|----------|
| A     | 0.0       | 0.0    | 0.0 | 0.0      |

## SL + CS (703 words)

### to CS (1414 words)

| Train | Precision | Recall | F1  | Accuracy |
|-------|-----------|--------|-----|----------|
| A     | 0.0       | 0.0    | 0.0 | 0.0      |


## EMPTY DATASET + CS (703)

| Train     | Precision | Recall | F1     | Accuracy |
|-----------|-----------|--------|--------|----------|
| CS only   | 0.0       | 0.0    | 0.0    | 0.9      |
| EN 10k    | 0.3688    | 0.3714 | 0.3701 | 0.8748   |
| SL 10k    | 0.4591    | 0.5214 | 0.4883 | 0.8918   |
| SL 100k   | 0.0       | 0.0    | 0.0    | 0.9      |


# Secondary Results

Here the data is still not used 100% correctly. Training data for Czech is `group_3_merged.csv` (about monkeys) and test data is the European union + Vanoce merged together (`pokus_data.csv`)

## Imbalance weight of loss function computation.

Computed as `1/2 * percentage` for each class

Test imbalance = `0.9`

### EN(1000) CS(700) - CS(1400)

Train imbalance = `0.88`


| imbalance_weight | precision | recall | f1 | accuracy |
| --- | --- | --- | --- | --- |
| 0.5 | 0.0000 | 0.0000 | 0.0000 | 0.9010 |
| 0.7 | 0.0000 | 0.0000 | 0.0000 | 0.9010 |
| 0.8 | 0.3562 | 0.1857 | 0.2441 | 0.8861 |
| 0.88 | 0.2318 | 0.6143 | 0.3366 | 0.7603 |
| 0.9 | 0.2233 | 0.6714 | 0.3351 | 0.7362 |
| 0.95 | 0.1019 | 0.9786 | 0.1846 | 0.1443 |


### EN(5000) CS(700) - CS(1400)

Train imbalance = `0.87`

| imbalance_weight | precision | recall | f1 | accuracy |
| --- | --- | --- | --- | --- |
| 0.75 | 0.4306 | 0.2214 | 0.2925 | 0.8939 |
| 0.8 | 0.3084 | 0.4714 | 0.3729 | 0.8430 |
| 0.85 | 0.2724 | 0.6286 | 0.3801 | 0.7970 |
| 0.88 | 0.3015 | 0.7214 | 0.4253 | 0.8069 |
| 0.9 | 0.2880 | 0.7571 | 0.4173 | 0.7907 |


### EN(10000) CS(700) - CS(1400)

Train imbalance = `0.872`

| imbalance_weight | precision | recall | f1 | accuracy |
| --- | --- | --- | --- | --- |
| 0.5 | 0.5745 | 0.1929 | 0.2888 | 0.9059 |
| 0.6 | 0.4884 | 0.3000 | 0.3717 | 0.8996 |
| 0.7 | 0.3614 | 0.4286 | 0.3922 | 0.8685 |
| 0.75 | 0.3750 | 0.4929 | 0.4259 | 0.8685 |
| 0.8 | 0.3110 | 0.5643 | 0.4010 | 0.8331 |
| 0.85 | 0.3127 | 0.7571 | 0.4426 | 0.8112 |
| 0.88 | 0.2593 | 0.7000 | 0.3784 | 0.7723 |
| 0.9 | 0.2349 | 0.7786 | 0.3609 | 0.7270 |




