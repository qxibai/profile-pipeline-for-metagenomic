# /usr/bin/python
import argparse
import os
import sys
from argparse import RawTextHelpFormatter

# variables
# 1. catalog_new: /home1/Laisenying/Data-analysis/CRC/03_SAM
# 2. output_path: /home1/Laisenying/Data-analysis/CRC/04_genecount

def parser():
  parser = argparse.ArgumentParser(description='generate gene count matrix', formatter_class=RawTextHelpFormatter)
  required = parser.add_argument_group('Required arguments')
  required.add_argument('-i', action='store', type=str, dest="catalog_new",
                        help='Path to folder of mapping results', required=True)
  required.add_argument('-o', action='store', type=str, dest="output_path",
                        help='Path to output folder', required=True)
  return parser
 

if __name__ == '__main__':
  args = parser().parse_args()
  # check arguments
  if os.path.isdir(args.catalog_new) != True:
      print("ERROR - The path of catalog folder is invalid: " + catalog_new)
      sys.exit()
  if os.path.isdir(args.output_path) != True:
      print("ERROR - The path of catalog folder is invalid: " + output_path)
      sys.exit()
  
  # check if the file under catalog directory is valid
  fileNames=[]
  if len(args.catalog_new) > 0:
    fileNames=os.listdir(args.catalog_new)
    if len(fileNames) == 0: # if no file under the folder
      print("ERROR - Catalog directory is empty:" + args.catalog_new)
      sys.exit()
      
  # print out arguments for users
  print("The path of new catalogs is "+ args.catalog_new)
  print("The output path is " + args.output_path)
  
  # get full path of all the sample catalogs
  full_path_fileNames = []
  # full_path_fileNames: /home1/Laisenying/Data-analysis/CRC/03_SAM/SRR162779
  for fileName in fileNames:
    full_path_fileNames.append(args.catalog_new + '/' + fileName)
    
  # start forming gene matrix
  count_sample = 0
  DNA_dictionary={}
  DNA_dictionary["geneName"]="gene_name"
  full_path_fileNames = sorted(full_path_fileNames)
  for fileName in full_path_fileNames:
    if os.path.exists(fileName + '/' + os.path.basename(fileName)+'.cat') is True:
      catalog_file = fileName + '/' + os.path.basename(fileName)+'.cat'
      inFile=open(catalog_file)
      data=inFile.readlines()
      # append sample names in the matrix
      DNA_dictionary["geneName"] = DNA_dictionary["geneName"] + "\t" + os.path.basename(fileName)
      # append the exact data
      for line in data:
        gene_name=line.split('\t')[0].rstrip()
        dna_readCount = line.split('\t')[3].rstrip()
        # DNA read counts
        if gene_name not in DNA_dictionary:
          DNA_dictionary[gene_name]=gene_name + "\t0"*count_sample
        DNA_dictionary[gene_name]=DNA_dictionary[gene_name]+'\t'+str(dna_readCount)
    else:
      print("the catalog sample " + os.path.bathname(fileName)+'.cat is missing')
      continue
    count_sample = count_sample + 1
    
    # append 0 to the gene not mapped
    # fix DNA matrix
    for key in DNA_dictionary:
      if len(DNA_dictionary[key].split('\t')) < count_sample + 1:
        DNA_dictionary[key] = DNA_dictionary[key]+'\t'+"0"
  
    # write matrics
    # DNA
    outFile_DNA = open(args.output_path+"/"+"DNA_hGEM.txt","w")
    outFile_DNA.write(DNA_dictionary["geneName"] + "\n")
    for key in DNA_dictionary:
      if key != "geneName":
        outFile_DNA.write(DNA_dictionary[key] + "\n")
        
