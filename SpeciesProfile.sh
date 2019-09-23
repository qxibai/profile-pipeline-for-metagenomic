#!/bin/bash

#$1: path to accs_id.txt
path_to_metaphlan2 = "/share/home1/Laisenying/miniconda3/envs/metaphlan2/"
BasePath = '/home1/Laisenying/Data-analysis/CRC'

source activate metaphlan2
cd $path_to_metaphlan2
for infile in `cat $1`
do
  metaphlan2.py \
    $BasePath/rmhuman/${infile}_hg38_paired_clean1.fq.gz,$BasePath/rmhuman/${infile}_hg38_paired_clean2.fq,gz \
    --bowtie2out $BasePath/02_bowtie/${infile}.bowtie2.bz2 \
    --nproc 8 \
    --input_type fastq > $BasePath/03_metaphlan2/${infile}.txt 
done  
