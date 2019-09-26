#!/usr/bin/env Rscript
# 1、annotation
# merge gene count txt and normalize by ref gene length
# KEGG annotation
# eggNOG annotation

options(warn = -1)
# see whether these packages exist on comp. If not, istall
package_list <- c("optparse")

for(p in package_list){
  if(!suppressWarnings(suppressMessages(require(p,character.only=TRUE,quietly=TRUE,warn.conflicts=FALSE)))){
    install.packages(p,repos="http://cran.r-project.org")
    suppressWarnings(suppressMessages(library(p,character.only=TRUE,quietly=TRUE,warn.conflicts=FALSE)))
  }
}
# 清理工作环境 clean environment object
rm(list=ls())

IGC_metadataPath = '/home1/Laisenying/.local/share/ngless/data/Modules/igc.ngm/0.9/IGC_metadata.Rdata'

# 加载依赖关系
library(optparse)
# 解析命令行
if(TRUE){
  option_list <- list(
    make_option(c("-i","--input"),type="character",help="path to runid list[/path/to/accs_id.txt]"),
    make_option(c("-o","--output"),type="character",help="path to output file")
  )
  opts <- parse_args(OptionParser(option_list=option_list))
  # 显示输入输出确认是否正确
  print(paste("The input file is ",opts$input,sep=""))
  print(paste("The output file prefix is",opts$output, sep = ""))
}


run_id  <- (read.table(opts$input))$V1
runid = run_id[1]
gene_Merge <- read.csv(paste('/home1/Laisenying/Data-analysis/CRC/04_genecount/',runid,'_GenesCount.csv',sep=''))
colnames(gene_Merge)[1] =  'gene'
for(runid in run_id[2:length(run_id)]){
  geneCount <- read.csv(paste('/home1/Laisenying/Data-analysis/CRC/04_genecount/',runid,'_GenesCount.csv',sep=''))
  colnames(geneCount)[1] =  'gene'
  gene_Merge <- merge(gene_Merge, geneCount, by='gene',all=TRUE)
}

save(gene_Merge,file = paste(opts$output,'/gene_profile.Rdata',sep=''))

# normalized
load(IGC_metadataPath)  #import IGC_metadata
rownames(IGC_metadata) = IGC_metadata$GeneName
rownames(gene_Merge) <- gene_Merge$gene
gene_Merge_normal <- gene_Merge[2:ncol(gene_Merge)]/(IGC_metadata[gene_Merge$gene,'GeneLength']/1000)
# save normalized gene profile data
save(gene_Merge_normal,paste(opts$output,'/gene_profile_normalized.Rdata',sep=''))

# KEGG annotation
gene_Merge_normal$KEGG <- IGC_metadata[gene_Merge$gene,'KEGGs']
KEGG_abundance <- apply(gene_Merge_normal[,-which(colnames(gene_Merge_normal) %in% c('KEGG'))],2,function(x){
  tapply(x, gene_Merge_normal[,"KEGG"],sum,na.rm=TRUE)
})
save(KEGG_abundance,paste(opts$output,'/KEGG_profile.Rdata',sep=''))

# eggNOE annotation
gene_Merge_normal$eggNOG <- IGC_metadata[gene_Merge$gene,'eggNOGs']
eggNOG_abundance <- apply(gene_Merge_normal[,-which(colnames(gene_Merge_normal) %in% c('KEGG','eggNOG'))],2,function(x){
  tapply(x, gene_Merge_normal[,"eggNOG"],sum,na.rm=TRUE)
})
save(eggNOG_abundance,paste(opts$output,'/eggNOG_profile.Rdata',sep=''))

