#!/bin/bash

Bwa='/home1/Laisenying/Tools/bwa/bwa'
ICG_database='/home1/Laisenying/.local/share/ngless/data/Modules/igc.ngm/0.9/igc.fna'
BasePath='/home1/Laisenying/Data-analysis/CRC'
SAMtools='/home1/Laisenying/Tools/samtools/samtools-1.9/samtools'
CountGene='/home1/Laisenying/Tools/gene_annotation/CountGene.py'

# 1、BWA-MEM alignment
for infile in `cat $1`
do
$Bwa mem -t 10 -R '@RG\tID:foo\tSM:bar\tLB:library' $ICG_database \
$BasePath/02_rmhuman/${infile}_hg38_paired_clean1.fq.gz \
$BasePath/02_rmhuman/${infile}_hg38_paired_clean2.fq.gz | $SAMtools view -@ 20 -S -F 4 -q 10 > $BasePath/03_SAM/${infile}.aligned.sam 

python $CountGene -i $BasePath/03_SAM/${infile}.aligned.sam  \
-o $BasePath/04_genecount \
-type all \
-min 50
done

