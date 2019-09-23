# profile-pipeline-for-metagenomic
mkdir 01_trim       #储存序列质控后的原始序列文件 \

mkdir 02_rmhuman    #比对到人类基因组上去除人类序列

mkdir 03_metaphlan2 #metaphlan2物种丰度注释文件

mkdir 03_bowtie2    #metaphlan2的中间输出文件

mkdir 04_humann2    #humann2功能注释结果文件 

mkdir 03_SAM        #与ICG gene catalog比对得到的SAM比对结果文件 \
mkdir 04_genecount  #对SAM结果文件进行统计得到的每一个样本的基因计数
mkdir 05_geneprofile # normalized后结果

required softwares: Bowtie2, Trimmomatic, BWA, Samtools, metaphlan2

