#!/bin/bash
#SBATCH --time 48:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16

velveth output 21 -fastq -short /data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R2_001_BC24EVACXX.filt.fastq
velvetg output -exp_cov auto -cov_cutoff auto