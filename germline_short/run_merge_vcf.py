
from glob import glob
import os
import subprocess as sp
import natsort


input_dir = r'/data_244/stemcell/WES/hardfilterd_vcf/dp_apply'

input_snp_format = r'hardFiltered_SNP*'
input_indel_format = r'hardFiltered_INDEL*'


snp_path_lst = natsort.natsorted(glob(os.path.join(input_dir, input_snp_format)))
indel_path_lst = natsort.natsorted(glob(os.path.join(input_dir, input_indel_format)))


print(snp_path_lst)
print(indel_path_lst)