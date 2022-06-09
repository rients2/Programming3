#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ri.dalstra@st.hanze.nl
#SBATCH --time 48:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=AssemblyAssignmentRients
#SBATCH --partition=assemblix

directory=/students/2021-2022/master/Rients_DSLS/output/
mkdir -p ${directory}

folder=${directory}


file1=/data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R1_001_BC24EVACXX.filt.fastq
file2=/data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R2_001_BC24EVACXX.filt.fastq

seq 25 2 27 | parallel -j16 velveth ${folder}{} {} -fastq -separate -longPaired ${file1} ${file2}
seq 25 2 27 | parallel -j16 velvetg ${folder}{}
seq 25 2 27 | parallel -j16 python3 assignment4.py -kmar {} >> output/kmars.csv

python3 assignment42.py

rm -r $folder*