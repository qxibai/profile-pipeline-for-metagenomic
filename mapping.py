# /usr/bin/python
import argparse
import os
import sys
import multiprocessing
from argparse import RawTextHelpFormatter

# variables
# 1. data_path: ./02_rmhuman
# 2. IGC_reference_database: /home1/Laisenying/.local/share/ngless/data/Modules/igc.ngm/0.9/igc.fna
# 3. output_path_intermediate: /home1/Laisenying/Data-analysis/CRC/03_SAM
# 7. sample_list: accs_id.txt
# 8. samtools_path: /home1/Laisenying/Tools/samtools/samtools-1.9
# 9. bedtools_path: /home1/Laisenying/Tools/bedtools2-2.25.0/bin
# 10.bwa_path: /home1/Laisenying/Tools/bwa


def parser():
  parser = argparse.ArgumentParser(description='mapping gene to IGC database and count genes', formatter_class=RawTextHelpFormatter)
  required = parser.add_argument_group('Required arguments')
  required.add_argument('-s', action='store', type=str, dest="data_path",
                        help='Path to fastq file for mapping', required=True)
  required.add_argument('-ref', action='store', type=str, dest="IGC_reference_database",
                        help='path to IGC reference database', required=True)
  required.add_argument('-o', action='store', type=str, dest="output_path_intermediate",
                        help='output directory for sam files, bam files and mapping coverage',
                        required=True)
  required.add_argument('-BWA', action='store', type=str, dest="bwa_path",
                        help='path to BWA',required=True)                      
  required.add_argument('-sam', action='store', type=str, dest="samtools_path",
                        help='path to samtools',
                        required=True)
  required.add_argument('-bed', action='store', type=str, dest="bedtools_path",
                        help='path to bedtools', required=True)
  required.add_argument('-list', action='store', type=str, dest="sample_list",
                        help='sample list: accs_id.txt', required=True)
  return parser



# define gene mapping pipeline
def BWA_mapping(provideDB_path, bwa_path, samtools_path, bedtools_path, DNA_first, DNA_second, output_path, fileName):
    # BWA-MEM
    if DNA_second == "false":  # single end
        os.system(bwa_path + "/bwa mem -t 15 " + provideDB_path + " " + DNA_first + " > " + output_path+"/"+fileName+".sam")
    else: # pair end
        os.system(bwa_path + "/bwa mem -t 15 " + provideDB_path + " " + DNA_first + " "+ DNA_second + " > " + output_path+"/"+fileName+".sam")
    # samtools
    os.system(samtools_path+"/samtools view -bS -q 10 " + output_path + "/" + fileName + ".sam > " + output_path + "/" + fileName + ".bam")
    os.system(samtools_path+"/samtools sort " + output_path + "/" + fileName + ".bam > " + output_path + "/" + fileName + ".bam.sort")
    if os.path.exists(provideDB_path + ".bed") is False:
        os.system("awk '/^>/ {if (seqlen){print \"0\t\"seqlen-1}; gsub(/^>/,\"\",$1);printf(\"%s\t\",$1) ;seqlen=0;next; } { seqlen += length($0)}END{print \"0\t\"seqlen-1}' " + provideDB_path + " > " + provideDB_path + ".bed")
    # bedtools calculate coverage
    os.system(bedtools_path + "/bedtools coverage -b " + output_path + "/" + fileName + ".bam.sort -a " + provideDB_path + ".bed > " + output_path + "/" + fileName + ".coverage")
    os.system("awk '{if ($3 + 0 != 0 && $7 + 0 != 0) print $1, $2, $3, $4, $5, $7}' OFS=\"\t\" " + output_path + "/" + fileName + ".coverage > " + output_path + "/" + fileName + ".cat")

    # delete useless file
    os.system("rm -rf " + output_path + "/" + fileName + ".sam")    
    os.system("rm -rf " + output_path + "/" + fileName + ".bam")  
    os.system("rm -rf " + output_path + "/" + fileName + ".coverage")  


if __name__ == '__main__':
    args = parser().parse_args()
    # check argument
    if os.path.isdir(args.data_path) is False:
        print("ERROR - The path of data directory is invalid: " + args.data_path)
        sys.exit()
    if os.path.exists(args.IGC_reference_database) is False:
        print("ERROR - The path of IGC reference database is invalid: " + args.IGC_reference_database)
        sys.exit()
    if os.path.isdir(args.IGC_reference_database) is True:
        print("ERROR - The path of IGC reference should be file instead of directory: " + args.IGC_reference_database)
        sys.exit()
    if os.path.isdir(args.output_path_intermediate) is False:
        print("ERROR - The path of alignment result directory is invalid: " + args.output_path_intermediate)
        sys.exit()

    # print out arguments for user
    print("The path of genome datasets is " + args.data_path)
    if len(args.IGC_reference_database) != 0:
        print("The path of reference database is " + args.IGC_reference_database)
    print("The alignment result directory is " + args.output_path_intermediate)
  

    # detecting datasets directory and processing them
    sample_list=open(args.sample_list, 'r')
    lines=sample_list.readlines()
    fileNames=[]
    for line in lines:
        line=line.strip()
        fileNames.append(line)

    DNA_first = ""
    DNA_second = ""
    processes = []
    for fileName in fileNames:
        # paired reads
        if os.path.exists(args.data_path+"/"+fileName+"_hg38_paired_clean1.fq.gz") is True and os.path.exists(args.data_path+"/"+fileName+"_hg38_paired_clean2.fq.gz") is True:
            DNA_first = args.data_path+"/"+fileName+"_hg38_paired_clean1.fq.gz"
            DNA_second = args.data_path+"/"+fileName+"_hg38_paired_clean2.fq.gz"
        elif os.path.exists(args.data_path+"/"+fileName+"_hg38_paired_clean.fq.gz") is True:
            DNA_first = args.data_path+"/"+fileName+"_hg38_paired_clean.fq.gz"
            DNA_second = "false"
        else:
            print("ERROR - the dataset: " + fileName + " missing metagenome files")
            continue

        # create output file
        if os.path.isdir(args.output_path_intermediate + "/" + fileName) is False:
            os.system("mkdir " + args.output_path_intermediate + "/" + fileName)

        print("Processing " + fileName)
        output_path = args.output_path_intermediate+"/"+fileName
        t = multiprocessing.Process(target=BWA_mapping, args=(args.IGC_reference_database, args.bwa_path,
                                                          args.samtools_path, args.bedtools_path, DNA_first, DNA_second,
                                                          output_path, fileName, ))
        processes.append(t)
        t.start()

    for one_process in processes:
        one_process.join()
