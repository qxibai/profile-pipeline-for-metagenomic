#!/bin/bash

# $1: path to accs_id.txt
TRIMMO_JAR_FILE='/home1/Laisenying/Tools/Trimmomatic-0.39/trimmomatic-0.39.jar'
TRIMMO_ADAPTOR_FILE_PE='/home1/Laisenying/Tools/Trimmomatic-0.39/adapters/TruSeq3-PE.fa'
Bowtie2='/home1/Laisenying/miniconda3/bin/bowtie2'
BasePath='/home1/Laisenying/Data-analysis/CRC'
Human_database='/home1/Laisenying/Tools/data/human/hg38'
TRIMMO_ADAPTOR_FILE_SE='/home1/Laisenying/Tools/Trimmomatic-0.39/adapters/TruSeq3-SE.fa'

export PATH=/usr/bin:$PATH

for infile in `cat $1`
do

if
[ -s "$BasePath/00_rawdata/${infile}/${infile}_1.fastq.gz" ] && [ -s "$BasePath/00_rawdata/${infile}/${infile}_2.fastq.gz" ] && [ ! -f "$BasePath/02_rmhumn/${infile}_hg38_paired_clean2.fq.gz" ];
then

java -jar $TRIMMO_JAR_FILE PE \
    -threads 8 \
    $BasePath/00_rawdata/${infile}/${infile}_1.fastq.gz  \
    $BasePath/00_rawdata/${infile}/${infile}_2.fastq.gz  \
    $BasePath/01_trim/${infile}_clean.1.fq.gz \
    $BasePath/01_trim/${infile}_clean_unpaired.1.fq.gz \
    $BasePath/01_trim/${infile}_clean.2.fq.gz \
    $BasePath/01_trim/${infile}_clean_unpaired.2.fq.gz \
    ILLUMINACLIP:$TRIMMO_ADAPTOR_FILE_PE:2:15:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:15:30 MINLEN:50

rm -rf $BasePath/01_trim/${infile}_clean_unpaired.1.fq.gz
rm -rf $BasePath/01_trim/${infile}_clean_unpaired.2.fq.gz

# 去宿主序列
$Bowtie2 -x $Human_database  \
    -p 8 \
    --very-sensitive \
    -1 $BasePath/01_trim/${infile}_clean.1.fq.gz \
    -2 $BasePath/01_trim/${infile}_clean.2.fq.gz \
    --un-conc-gz $BasePath/02_rmhuman/${infile}_hg38_paired_clean%.fq.gz \
    --al-conc-gz $BasePath/02_rmhuman/${infile}_hg38_paired_contam%.fq.gz 
    
rm -rf $BasePath/02_rmhuman/${infile}_hg38_paired_contam1.fq.gz 
rm -rf $BasePath/02_rmhuman/${infile}_hg38_paired_contam2.fq.gz 

elif
[ -s "$BasePath/00_rawdata/${infile}/${infile}.fastq.gz" ] && [ ! -f "$BasePath/00_rawdata/${infile}/${infile}_1.fastq.gz" ] && [ ! -f "$BasePath/02_rmhumn/${infile}_hg38_paired_clean.fq.gz" ];
then

java -jar $TRIMMO_JAR_FILE SE \
    -threads 8 \
    $BasePath/00_rawdata/${infile}/${infile}.fastq.gz  \
    $BasePath/01_trim/${infile}_clean.fq.gz \
    ILLUMINACLIP:$TRIMMO_ADAPTOR_FILE_SE:2:15:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:15:30 MINLEN:50


# 去宿主序列
$Bowtie2 -x $Human_database  \
    -p 8 \
    --very-sensitive \
    -U $BasePath/01_trim/${infile}_clean.fq.gz \
    --un-gz $BasePath/02_rmhuman/${infile}_hg38_paired_clean.fq.gz \
    --al-gz $BasePath/02_rmhuman/${infile}_hg38_paired_contam.fq.gz 
    
rm -rf $BasePath/02_rmhuman/${infile}_hg38_paired_contam.fq.gz 
fi

# remove file in 00_rawdata and 01_trim to save space
if
[ -s "$BasePath/02_rmhuman/${infile}_hg38_paired_clean.fq.gz" ];
then
rm -rf $BasePath/01_trim/${infile}_clean.fq.gz
rm -rf $BasePath/00_rawdata/${infile}/${infile}.fastq.gz
elif
[ -s "$BasePath/02_rmhuman/${infile}_hg38_paired_clean1.fq.gz" ] && [ -s "$BasePath/02_rmhuman/${infile}_hg38_paired_clean2.fq.gz" ];
then
rm -rf $BasePath/01_trim/${infile}_clean.1.fq.gz
rm -rf $BasePath/01_trim/${infile}_clean.2.fq.gz
rm -rf $BasePath/00_rawdata/${infile}/${infile}_1.fastq.gz
rm -rf $BasePath/00_rawdata/${infile}/${infile}_2.fastq.gz
fi

done






