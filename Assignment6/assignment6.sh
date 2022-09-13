#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ri.dalstra@st.hanze.nl
#SBATCH --time 48:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16

#SBATCH --job-name=Assignment6Rients
#SBATCH --partition=assemblix


python3 python_files/question1.py >> output/answers.csv
python3 python_files/question5.py >> output/answers.csv
