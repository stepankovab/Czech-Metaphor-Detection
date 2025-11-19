#!/bin/bash
#PBS -q default@pbs-m1.metacentrum.cz
#PBS -l walltime=24:0:0
#PBS -l select=1:ncpus=1:ngpus=1:mem=20gb:scratch_local=20gb
#PBS -N ES100-ES

module add mambaforge
conda activate /storage/brno2/home/stepanb2/.conda/envs/deeplearning

DATADIR=/storage/brno2/home/stepanb2/Czech-Metaphor-Detection

python $DATADIR/Experiments/mBERT_training/mBERT_training.py --train_languages es --train_counts 100 --test_language es --test_count 726 --output_dir $DATADIR/out --source_dir $DATADIR --model_name bert-base-multilingual-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss focal

clean_scratch
