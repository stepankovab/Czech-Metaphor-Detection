#!/bin/bash
#PBS -q default@pbs-m1.metacentrum.cz
#PBS -l walltime=24:0:0
#PBS -l select=1:ncpus=1:ngpus=1:mem=20gb:scratch_local=20gb:gpu_cap=sm_90
#PBS -N language_permutations_mm

module add mambaforge
conda activate /storage/brno2/home/stepanb2/.conda/envs/cuda-new

DATADIR=/storage/brno2/home/stepanb2/Czech-Metaphor-Detection


python $DATADIR/Experiments/model_training/model_training.py --train_languages es en sl cs --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages es sl en cs --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages es en cs sl --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages es sl cs en --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages es cs en sl --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages es cs sl en --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted





python $DATADIR/Experiments/model_training/model_training.py --train_languages en es sl cs --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages en es cs sl --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages en sl cs es --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages en sl es cs --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages en cs es sl --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages en cs sl es --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted










python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs en es --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl cs es en --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl en es cs --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl en cs es --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl es cs en --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages sl es en cs --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted










python $DATADIR/Experiments/model_training/model_training.py --train_languages cs es en sl --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages cs es sl en --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages cs en sl es --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages cs en es sl --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages cs sl es en --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted

python $DATADIR/Experiments/model_training/model_training.py --train_languages cs sl en es --train_counts 20000 20000 20000 20000 --test_language cs --test_count 10000 --output_dir $DATADIR/out --source_dir $DATADIR --model_name jhu-clsp/mmBERT-base --seed 42 --imbalance_weight 0.5 --epochs 3 --train_batch_size 32 --test_batch_size 32 --learning_rate 3e-5 --weight_decay 0.01 --warmup_ratio 0.06 --loss weighted


clean_scratch
