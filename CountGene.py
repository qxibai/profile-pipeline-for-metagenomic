# /usr/bin/python
import pandas as pd
import re
import argparse
import os
from argparse import RawTextHelpFormatter

# Command Line Argument Parsing
def parser():
  parser = argparse.ArgumentParser(description='Gene Count pipeline.', formatter_class=RawTextHelpFormatter)
  required = parser.add_argument_group('Required arguments')
  optional = parser.add_argument_group('Optional arguments')
  required.add_argument('-i', action='store', type=str, dest="samfile", help='Path to SAM file of read alignment', required=True)
  required.add_argument('-o', action='store', type=str, dest="output_folder", help='Output Path', required=True)
  required.add_argument('-q', action='store', default=5, type=int, dest="mapq", help='mapQ of alignment', required=False)
  required.add_argument('-type', action='store',type=str, dest="count_type", default='union',
                        help='methods of counting reads mapped to reference gene[union. strict], Default: union',
                        required=False)
  required.add_argument('-min', action='store', type=int, dest="min_length", default=50,
                        help='min length of mapped part, Default: 50[bp]',
                        required=False)
  return parser


# 读取SAM格式文件
def filetodata(samfile):
    fileout = open(samfile, 'r')
    lines = fileout.readlines()
    read_id = []
    flag = []
    gene = []
    pos = []
    mapq = []
    mlen = []
    CIGAR = []
    pair_gene = []
    pair_pos = []
    mapped_length = []
    for line in lines:
        line = line.strip()
        linetolist = line.split('\t')
        read_id.append(linetolist[0])
        flag.append(linetolist[1])
        gene.append(linetolist[2])
        pos.append(int(linetolist[3]))
        mapq.append(int(linetolist[4]))
        mlen.append(sum(map(int, re.findall(re.compile('([0-9]+)M', re.DOTALL), linetolist[5]))))
        CIGAR.append(linetolist[5])
        pair_gene.append(linetolist[6])  #"=": paired_read都比对到同一个基因
        pair_pos.append(int(linetolist[7]))
        mapped_length.append(int(linetolist[8]))
    dictory = {'read_id': read_id, 'flag': flag, 'gene': gene, 'pos': pos, 'mapq': mapq, 'CIGAR': CIGAR, 'mlen': mlen,
               'pair_gene': pair_gene, 'pair_pos': pair_pos, 'mapped_length': mapped_length}
    dataSAM = pd.DataFrame(dictory)
    return dataSAM


def filter_reads(dataSAM, count_type='union', min_length=50):
    if count_type == 'union':
        """
        both ends or single read with enough mapped length from a read pair mapped to unique gene 
        """
        dataSAM_fil = dataSAM[dataSAM['pair_gene'] == '=']
        dataSAM_fil = dataSAM_fil[dataSAM_fil['mlen'] >= min_length]
        return dataSAM_fil
    
    if count_type == 'strict':
        """
        both ends from a read pair mapped to a gene 
        """
        dataSAM_fil = dataSAM[abs(dataSAM['mapped_length']) >= min_length]
        return dataSAM_fil
        
    if count_type == 'single':
      dataSAM_fil = dataSAM_fil[dataSAM_fil['mlen'] >= min_length]
      

# count the number of reads mapped to the gene
def gene_counts():
    print("read SAMfile···")
    dataSAM = filetodata(args.samfile)
    print("filter reads···")
    dataSAM_fil = filter_reads(dataSAM, args.count_type, args.min_length)
    print("count genes···")
    dataSAM_rdup = dataSAM_fil.drop_duplicates(['read_id'])
    counts = dataSAM_rdup['gene'].value_counts()
    sample_name = re.findall(re.compile('([A-Z0-9]+)', re.DOTALL), os.path.basename(args.samfile))[0]
    counts = pd.DataFrame(counts).rename(columns={'gene': sample_name})
    counts.to_csv(args.output_folder + "/" + sample_name + "_GenesCount.csv")


if __name__ == '__main__':
    args = parser().parse_args()
    gene_counts()

