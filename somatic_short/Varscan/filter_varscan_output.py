from logging import root
import os
from glob import glob
import subprocess as sp
import pandas as pd



root_dir = r'/data/stemcell/WES/GRCh38/bamfiles/mpileup_files/varscan_vcf/indel'

file_format = '*.indel'
ref_genome = r'/data/refGenome/hg38/v0/gdc/GRCh38.d1.vd1.fa'

sh_path = r'/data/src/DNASEQ-pipeline/somatic_short/Varscan/varscan_somatic_filter.sh'

output_dir_name = 'filtered'
output_dir_path = os.path.join(root_dir, output_dir_name)
qsub_log_dir_name = 'filter_log'


##################### qsub 환경설정 ###################################

pbs_N = "varscan_filter"
pbs_o = os.path.join(root_dir, qsub_log_dir_name)
pbs_j = "oe"
pbs_l_core = 2

######################################################################

if os.path.isdir(output_dir_path) is False:
    os.mkdir(output_dir_path)

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)



file_list = glob(os.path.join(root_dir, file_format))

# print(file_list)



for vcf_file in file_list:
    sample_name = vcf_file.split(r'/')[-1].split(r'.')[0]
    print(sample_name)
    
    output_name = sample_name + '_filtered.vcf'
    output_path = os.path.join(output_dir_path, output_name)
    
    # sp.call(f'varscan somatic {normal_pileup} {tumor_pileup} {sample_name}')
    
    sp.call(f'echo "sh {sh_path} {vcf_file} {output_path}" | \
        qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
    