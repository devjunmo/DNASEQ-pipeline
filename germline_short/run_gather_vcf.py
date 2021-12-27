

###############################################
# 사용 안함. 그냥 커맨드라인으로 노가다로 할것 #
###############################################


# chr 단위로 joint calling 진행 이후 vcf file들을 하나로 gather



import os
from glob import glob
import pandas as pd
import subprocess as sp

SRC_PATH = r'/data_244/src/ips_germ_210805/DNASEQ-pipeline/germline_short/gather_vcf.sh'

input_dir = r'/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/GVCF/genomic_DB/joint_call'
output_dir_name = r'gather'
output_vcf_name = r'stemcell_whole_samples.vcf.gz'

vcf_prefix = r'stemcell_jointCall_chr'
vcf_suffix = r'.vcf.gz'

out_dir = os.path.join(input_dir, output_dir_name)

if os.path.isdir(out_dir) is False:
    os.mkdir(out_dir)

output_vcf_path = os.path.join(out_dir, output_vcf_name)

input_prefix = os.path.join(input_dir, vcf_prefix)

chr_lst = list(range(1,23)) # 1~22 
chr_lst.append('X')
chr_lst.append('Y')

chr_lst = list(map(str, chr_lst))
chr_lst = list(map(lambda x: input_prefix + x + vcf_suffix, chr_lst))

# print(chr_lst)

input_str = ' '.join(chr_lst)
print(input_str)

# exit(0)
# !! BACKUP YOUR JOINT CALL OUTPUT FILES !! 
# sp.call(f'nohup sh {SRC_PATH} {input_str} {output_vcf_path} &', shell=True)

