#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ri.dalstra@st.hanze.nl
#SBATCH --time 2:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=BlastAssignmentRients
#SBATCH --partition=assemblix

mkdir -p output
echo '' > output/timings.txt
echo '' > output/output_blast.txt
export BLASTDB=/local-fs/datasets/refseq_protein/refseq_protein
export time=/usr/bin/time
export time_file=output/timings.txt
export output=output/output_blast.txt

for n in {1..16}
do
$time --append -o $time_file -f ${n}'\t'%e blastp -query MCRA.faa -db $BLASTDB -num_threads $n -outfmt 6 >> $output
echo 'done with' $n 
done

python3 assignment3.py


