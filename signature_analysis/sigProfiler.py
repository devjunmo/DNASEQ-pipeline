

from SigProfilerMatrixGenerator import install as genInstall
from SigProfilerExtractor import sigpro as sig
import os


old_wd = os.getcwd()
# os.chdir(r'/home/jun9485/data/utuc/somatic_call/filtered/snp')

# root_dir = r'/home/jun9485/data/utuc/somatic_call/filtered/'
# root_dir = r'/home/jun9485/'
# root_dir = r'/home/jun9485/data/utuc/somatic_call_mutect1/filtered_vcf/'
root_dir = r'/home/jun9485/data/utuc/somatic_call/filtered/indel/'

# input_dir_name = r'snp/'
# input_dir_name = r'ejTest/'
input_dir_name = r'vcf/'

os.chdir(root_dir)

os.getcwd()


# input_vcf_dir = '/home/jun9485/data/utuc/somatic_call/filtered/snp/'

# path_to_example_table = sig.importdata("vcf")

# path_to_example_table = sig.importdata("vcf")
# print(path_to_example_table)

out_dir_name = r'sig_analysis/'

# input_dir_name = r''

input_dir = root_dir + input_dir_name

sig.sigProfilerExtractor('vcf', out_dir_name, input_dir)

os.chdir(old_wd)