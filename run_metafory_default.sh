#!/bin/bash
#PBS -q default@pbs-m1.metacentrum.cz
#PBS -l walltime=24:0:0
#PBS -l select=1:ncpus=1:ngpus=1:mem=20gb:scratch_local=20gb:gpu_cap=sm_90
#PBS -N cs_to_en

module add mambaforge
conda activate /storage/brno2/home/stepanb2/.conda/envs/cuda-new

DATADIR=/storage/brno2/home/stepanb2/Czech-Metaphor-Detection

python $DATADIR/Experiments/model_training/model_training.py --train_languages en --train_counts 12000 --test_language cs_en --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted



clean_scratch
