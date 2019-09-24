#!/bin/bash

#$1: path to accs_id.txt
path_to_metaphlan2="/share/home1/Laisenying/miniconda3/envs/metaphlan2/"
BasePath='/home1/Laisenying/Data-analysis/CRC'
chocophlan_database='/share/home1/Laisenying/Tools/data/humann2/chocophlan'
uniref_database='/share/home1/Laisenying/Tools/data/humann2/uniref'
HuMann2='/home1/Laisenying/miniconda3/bin/humann2'

export PATH=/share/home1/Laisenying/Tools:$PATH
for infile in `cat $1`
do
  cat $BasePath/02_rmhuman/${infile}_hg38_paired_clean1.fq.gz $BasePath/02_rmhuman/${infile}_hg38_paired_clean2.fq.gz > $BasePath/04_combined/${infile}_combined.fq.gz
  $HuMann2 --input $BasePath/04_combined/${infile}_combined.fq.gz \
    --nucleotide-database $chocophlan_database \
    --protein-database $uniref_database \
    --verbose \
    --threads 20 \
    --remove-temp-output \
    --taxonomic-profile $BasePath/03_metaphlan2/${infile}.txt \
    --output-basename ${infile}_humann2 \
    --output $BasePath/humann2_result/${infile}
  rm -rf $BasePath/04_combined/${infile}_combined.fq.gz
done
