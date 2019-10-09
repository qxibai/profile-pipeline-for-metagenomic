# profile-pipeline-for-metagenomic
#### 需要提前准备的文件目录，放在同一目录下
##### 序列质控
mkdir 00_rawdata    #原始序列文件 \
mkdir 01_trim       #储存序列质控后的原始序列文件 \
mkdir 02_rmhuman    #比对到人类基因组上去除人类序列 
##### species profile
mkdir 03_metaphlan2 #metaphlan2物种丰度注释文件 \
mkdir 03_bowtie2    #metaphlan2的中间输出文件 
##### functional profile
mkdir 04_humann2    #humann2功能注释结果文件 \
mkdir 04_combined   #存放中间文件 \
mkdir 03_SAM        #与ICG gene catalog比对得到的SAM比对结果文件 
##### gene profile
mkdir 04_genecount  #对SAM结果文件进行统计得到的每一个样本的基因计数 \
mkdir 05_geneprofile # normalized后结果 

#### required softwares: 
- Bowtie2
- Trimmomatic
- BWA
- bedtools
- Samtools
- metaphlan2 
- humann2

#### required DataBase:
 - Human Genome database: /home1/Laisenying/Tools/data/human/hg38
 - ICG gene catalog: /home1/Laisenying/.local/share/ngless/data/Modules/igc.ngm/0.9/igc.fna
 - chorophlan database: /share/home1/Laisenying/Tools/data/humann2/chocophlan
 - uniref database: /share/home1/Laisenying/Tools/data/humann2/uniref
 

1、------ 原始序列质量控制，并去除宿主(人类)序列 ------
```
./preprocess.sh accs_id.txt 
```
accs_id.txt : 存放NCBI run_id 的txt文件

2. ------ generate species profile ------------- 
```
./SpeciesProfile.sh accs_id.txt
```

3. ----- generate functional profile ----------
```
./FunctionalProfile.sh accs_id.txt
```

4. ----- generate Gene profile ------
```
python bowtie2_mapping.py \
  -s /home1/Laisenying/Data-analysis/CRC/02_rmhuman \
  -ref /home1/Laisenying/.local/share/ngless/data/Modules/igc.ngm/0.9/igc.fna \
  -o /home1/Laisenying/Data-analysis/CRC/03_SAM \
  -BWA /home1/Laisenying/Tools/bwa \
  -sam /home1/Laisenying/Tools/samtools/samtools-1.9 \
  -bed /home1/Laisenying/Tools/bedtools2-2.25.0/bin \
  -list /home1/Laisenying/Data-analysis/CRC/accs_id2.txt
```

