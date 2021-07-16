

from SigProfilerMatrixGenerator import install as genInstall
from SigProfilerExtractor import sigpro as sig
import os


old_wd = os.getcwd()
os.chdir(r'/home/jun9485/data/utuc/somatic_call/filtered/snp')
os.getcwd()


# input_vcf_dir = '/home/jun9485/data/utuc/somatic_call/filtered/snp/'

# path_to_example_table = sig.importdata("vcf")

path_to_example_table = sig.importdata("vcf")
print(path_to_example_table)

out_dir_name = r'sig_analysis/'

# input_dir_name = r''



sig.sigProfilerExtractor('vcf', out_dir_name, path_to_example_table)

os.chdir(old_wd)