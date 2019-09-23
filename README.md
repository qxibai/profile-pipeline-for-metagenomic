# profile-pipeline-for-metagenomic
# 需要提前准备的文件目录，放在同一目录下
# 序列质控
mkdir 00_rawdata    #原始序列文件
mkdir 01_trim       #储存序列质控后的原始序列文件 \
mkdir 02_rmhuman    #比对到人类基因组上去除人类序列 \
# species profile
mkdir 03_metaphlan2 #metaphlan2物种丰度注释文件 \
mkdir 03_bowtie2    #metaphlan2的中间输出文件 \
# functional profile
mkdir 04_humann2    #humann2功能注释结果文件 \
mkdir 03_SAM        #与ICG gene catalog比对得到的SAM比对结果文件 \
# gene profile
mkdir 04_genecount  #对SAM结果文件进行统计得到的每一个样本的基因计数 \
mkdir 05_geneprofile # normalized后结果 \

required softwares: Bowtie2, Trimmomatic, BWA, Samtools, metaphlan2 \
required DataBase:
 - Human Genome: hg38
 

1、------ 原始序列质量控制，并去除宿主(人类)序列 ---------
