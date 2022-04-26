from logging import root
import os
from glob import glob
import subprocess as sp
import pandas as pd



root_dir = r'/data/stemcell/WES/GRCh38/bamfiles/ips35I'

file_format = '*.bam'
ref_genome = r'/data/refGenome/hg38/v0/gdc/GRCh38.d1.vd1.fa'

output_dir_name = 'mpileup_files'
output_dir_path = os.path.join(root_dir, output_dir_name)

file_path = os.path.join(root_dir, file_format)

file_list = glob(file_path)

##################### qsub 환경설정 ###################################

pbs_N = "mk_mpileup"
pbs_o = os.path.join(root_dir, 'mpileup_logs')
pbs_j = "oe"
pbs_l_core = 2
######################################################################

if os.path.isdir(output_dir_path) is False:
    os.mkdir(output_dir_path)

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)
    
    
for bam_file_path in file_list:
    print(bam_file_path)
    
    sample_name = bam_file_path.split(r'/')[-1].split('_')[0]
    
    print(sample_name)
    
    output_name = sample_name + '.mpileup'
    
    output_path = os.path.join(output_dir_path, output_name)

    # sp.call(f'samtools mpileup -f {ref_genome} {bam_file_path} > {output_path}')
    
    sp.call(f'echo "samtools mpileup -f {ref_genome} {bam_file_path} > {output_path}" | \
        qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
    

