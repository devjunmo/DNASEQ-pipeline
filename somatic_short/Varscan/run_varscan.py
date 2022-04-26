from logging import root
import os
from glob import glob
import subprocess as sp
import pandas as pd



root_dir = r'/data/stemcell/WES/GRCh38/bamfiles/mpileup_files/ips35I_varscanRE'

file_format = '*.mpileup'
ref_genome = r'/data/refGenome/hg38/v0/gdc/GRCh38.d1.vd1.fa'

sh_path = r'/data/src/DNASEQ-pipeline/somatic_short/Varscan/varscan.sh'


pair_info = r'/data/stemcell/WES/GRCh38/stemcell_WES_sample_pair_220318.csv'
pair_info_tumor_col_name = 'Tumor'
pair_info_normal_col_name = 'Normal'


output_dir_name = 'varscan_output'
output_dir_path = os.path.join(root_dir, output_dir_name)
qsub_log_dir_name = 'varscan_log'


##################### qsub 환경설정 ###################################

pbs_N = "varscan"
pbs_o = os.path.join(root_dir, qsub_log_dir_name)
pbs_j = "oe"
pbs_l_core = 2

######################################################################

if os.path.isdir(output_dir_path) is False:
    os.mkdir(output_dir_path)

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)


pair_df = pd.read_csv(pair_info)
print(pair_df)
pair_df.set_index(pair_info_tumor_col_name, inplace=True)
pair_dict = pair_df.to_dict('index') # {tumor : {normal:_ grade:_} dict 형태. fname

print(pair_df)
print(pair_dict)



file_list = glob(os.path.join(root_dir, file_format))



for mpileup_file in file_list:
    print(mpileup_file)
    sample_name = mpileup_file.split(r'/')[-1].split(r'.')[0]
    print(sample_name)
    
    output_name = sample_name
    
    
    
    try:
        normal_sample_name = pair_dict[sample_name]['Normal']
    except KeyError:
        continue
    
    normal_pileup = normal_sample_name + '.mpileup'
    
    tumor_pileup = sample_name + '.mpileup'
    
    print(normal_pileup)
    print(tumor_pileup)
    
    # sp.call(f'varscan somatic {normal_pileup} {tumor_pileup} {sample_name}')
    
    sp.call(f'echo "sh {sh_path} {normal_pileup} {tumor_pileup} {sample_name} {root_dir}" | \
        qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
    