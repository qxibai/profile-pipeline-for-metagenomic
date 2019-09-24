#!/bin/bash

accs_id='/home1/Laisenying/Data-analysis/CRC/test.txt'
Bwa='/home1/Laisenying/Tools/bwa/bwa'
ICG_databas='/home1/Laisenying/.local/share/ngless/data/Modules/igc.ngm/0.9/igc.fna'
BasePath='/home1/Laisenying/Data-analysis/CRC'
SAMtools='/home1/Laisenying/Tools/samtools/samtools-1.9/samtools'
CountGene='/home1/Laisenying/Tools/gene_annotation/CountGene.py'

# 1、BWA-MEM alignment
for infile in `cat $1`
do
if
[ -s "$BasePath/02_rmhuman/${infile}_hg38_paired_clean1.fq.gz" ] && [ -s "$BasePath/02_rmhuman/${infile}_hg38_paired_clean2.fq.gz" ];
then

  $Bwa mem -t 10 -R '@RG\tID:foo\tSM:bar\tLB:library' $ICG_databas \
  $BasePath/02_rmhuman/${infile}_hg38_paired_clean1.fq.gz \
  $BasePath/02_rmhuman/${infile}_hg38_paired_clean2.fq.gz | $SAMtools view -@ 5 -S -F 4 -q 10 > $BasePath/03_SAM/${infile}.aligned.sam 

  python /home1/Laisenying/Tools/gene_annotation/CountGene.py -i $BasePath/03_SAM/${infile}.aligned.sam  \
    -o $BasePath/04_genecount \
    -type strict \
    -min 50
    
elif
[ -s "$BasePath/02_rmhuman/${infile}_hg38_paired_clean.fq.gz" ] && [! -f "$BasePath/02_rmhuman/${infile}_hg38_paired_clean1.fq.gz" ];
then

  $Bwa mem -t 10 -R '@RG\tID:foo\tSM:bar\tLB:library' $ICG_databas \
  $BasePath/02_rmhuman/${infile}_hg38_paired_clean.fq.gz | $SAMtools view -@ 5 -S -F 4 -q 10 > $BasePath/03_SAM/${infile}.aligned.sam 


python /home1/Laisenying/Tools/gene_annotation/CountGene.py -i $BasePath/03_SAM/${infile}.aligned.sam  \
    -o $BasePath/04_genecount \
    -type single \
    -min 50
done

