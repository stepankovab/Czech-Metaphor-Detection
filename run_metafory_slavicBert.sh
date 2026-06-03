#!/bin/bash
#PBS -q default@pbs-m1.metacentrum.cz
#PBS -l walltime=24:0:0
#PBS -l select=1:ncpus=1:ngpus=1:mem=20gb:scratch_local=20gb:gpu_cap=sm_90
#PBS -N SlavicBert_SLCS-CS

module add mambaforge
conda activate /storage/brno2/home/stepanb2/.conda/envs/cuda-new

DATADIR=/storage/brno2/home/stepanb2/Czech-Metaphor-Detection



python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 10 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 50 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 100 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 200 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 300 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 400 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 500 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 750 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 1000 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 1500 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 2000 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 3000 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 6000 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 9000 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs --train_counts 12000 1000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name DeepPavlov/bert-base-bg-cs-pl-ru-cased --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted


clean_scratch
