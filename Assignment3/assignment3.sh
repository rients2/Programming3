for THREAD in {1..16} do blastp -query MCRA.faa -db refseq_protein/refseq_protein -num_threads THREAD -outfmt 6 >> blastoutput.txt;
