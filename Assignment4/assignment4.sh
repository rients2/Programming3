#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ri.dalstra@st.hanze.nl
#SBATCH --time 48:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=BlastAssignmentRients
#SBATCH --partition=assemblix

velveth directory 21 -fastq -short /data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R2_001_BC24EVACXX.filt.fastq
velvetg directory -exp_cov auto -cov_cutoff auto