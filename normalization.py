# /usr/bin/python
import argparse
import copy
from argparse import RawTextHelpFormatter

# variable 
# IGC_reference_database="/home1/Laisenying/.local/share/ngless/data/Modules/igc.ngm/0.9/igc.fna"
# gene_matrix='/home1/Laisenying/Data-analysis/CRC/04_genecount/DNA_hGEM.txt'
# output_path='/home1/Laisenying/Data-analysis/CRC/05_geneprofile'
# cutoff_value = 1.0
# sample_value = 1

def parser():
  parser = argparse.ArgumentParser(description='TPM normalization and filtered', formatter_class=RawTextHelpFormatter)
  required = parser.add_argument_group('Required arguments')
  required.add_argument('-i', action='store', type=str, dest="gene_matrix",
                        help='hGEM gene matrix', required=True)
  required.add_argument('-minTPM', action='store', type=float, dest="cutoff_value",
                        help='min TPM', required=False,default=1.0)
  required.add_argument('-minSam', action='store', type=int, dest="sample_value",
                        help='min samples', required=False,default=1)                      
  required.add_argument('-ref', action='store', type=str, dest="IGC_reference_database",
                        help='path to IGC reference database', required=True) 
  required.add_argument('-o', action='store', type=str, dest="output_path",
                        help='path to output folder', required=True)                       
  return parser                  
  
# return true if at least one element greater than cut off value
# return false if all element less than cut off value
def keep_this_line(aList):
    count = 0
    for element in aList:
        if float(element) >= args.cutoff_value:
            count = count + 1
    if count >= args.sample_value:
        return True
    else:
        return False

                        

if __name__ == '__main__':
  args = parser().parse_args()
  if args.cutoff_value == 1:
    print("the default TPM cut-off value is 1")
  else:
    print("the TPM cut-off value is " + str(args.cutoff_value))
    
  # get gene length
  IGC_reference_database_file = open(args.IGC_reference_database)
  IGC_reference = IGC_reference_database_file.readlines()
  dictionary = {}
  count = 0  
  while count < len(IGC_reference):
    if IGC_reference[count][0] == '>': # it is the header of the sequence
        gene_name = IGC_reference[count].split()[0][1:]
        dictionary[gene_name] = len(IGC_reference[count + 1]) - 1
        temp_count = count + 2
        while temp_count < len(IGC_reference) and IGC_reference[temp_count][0] != '>':
            dictionary[gene_name] = dictionary[gene_name] + len(IGC_reference[temp_count]) - 1
            temp_count = temp_count + 1
    
    count = count + 1
    
    
  # processing DNA matrix
  DNA_matrix_file = open(args.gene_matrix)
  DNA_matrix_data = DNA_matrix_file.readlines()
  DNA_matrix_length_before_filter = len(DNA_matrix_data) - 1
  DNA_matrix_data_original = copy.deepcopy(DNA_matrix_data)
    
  row = 0
  column = 0
    
  # convert DNA_matrix_data to the matrix
  while row < len(DNA_matrix_data):
    DNA_matrix_data[row] = DNA_matrix_data[row].split()
    row = row + 1
      
  # start calculating TPM
  row = 1
  column = 1
  # step 1 divide read counts by gene length in kilobase
  while row < len(DNA_matrix_data):
    column=1
    while column < len(DNA_matrix_data[0]):
        gene_name = DNA_matrix_data[row][0]
        gene_length = dictionary[gene_name]
        DNA_matrix_data[row][column] = str( float( DNA_matrix_data[row][column] ) /  ( float(gene_length) / 1000) )
        column = column + 1
    row = row + 1
      
  # step 2: Count up all the RPK values in a sample and divide this number by 1,000,000
  scaling_factor = []
  scaling_factor.append(0)
  row = 1
  column = 1
  while column < len(DNA_matrix_data[0]):
    row = 1
    total=0.0
    while row < len(DNA_matrix_data):
      total = total + float(DNA_matrix_data[row][column])
      row = row + 1
      
    scaling_factor.append(total/1000000)
    column = column + 1
    
  # step 3
  row = 1
  column = 1
  while column < len(DNA_matrix_data[0]):
    row = 1
    while row < len(DNA_matrix_data):
      if(scaling_factor[column] == 0):
        DNA_matrix_data[row][column] = "0"
      else:
        DNA_matrix_data[row][column] = str( float( DNA_matrix_data[row][column] ) / scaling_factor[column] )
      row = row + 1
    column = column + 1
        
  # filter TPM
  # write to the file
  DNA_matrix_outFile = open(args.output_path + "/DNA_hGEM_filt.txt", "w")
  DNA_matrix_outFile.write(DNA_matrix_data_original[0])
  count = 1
  DNA_matrix_length_after_filter = 0
  while count < len(DNA_matrix_data_original):
    if keep_this_line(DNA_matrix_data[count][1:]) == True:
        DNA_matrix_data[count].append('\n')
        DNA_matrix_outFile.write("\t".join(DNA_matrix_data[count]))
        DNA_matrix_length_after_filter = DNA_matrix_length_after_filter + 1
    count = count + 1
    
  DNA_matrix_file.close()
  DNA_matrix_outFile.close()
  
  # write summary file
  outFile_summary = open(args.output_path + "/hGEM_filt.summary", "w")
  outFile_summary.write("DNA TPM filtering:\n")
  rate = float((DNA_matrix_length_before_filter - DNA_matrix_length_after_filter) / float(DNA_matrix_length_before_filter)) * 100
  outFile_summary.write("Total: " + str(DNA_matrix_length_before_filter) + " genes\tRemoval: " + str(DNA_matrix_length_before_filter - DNA_matrix_length_after_filter) + " genes\tRemaining: " + str(DNA_matrix_length_after_filter) + " genes\tFilter_rate: " + str(rate) + "\n\n")

    
   
