import pandas as pd
import os
from glob import glob
import subprocess as sp



root_dir = r'/data/stemcell/WES/GRCh38/bamfiles'

file_format = '*.bam'
ref_genome = r'/data/refGenome/hg38/v0/gdc/GRCh38.d1.vd1.fa'

target = r'/data/refGenome/CNVkit/S07604514_Padded.bed'
access = r'/data/refGenome/CNVkit/access.GRch38.bed'

sh_path = r'/data/src/DNASEQ-pipeline/CNV/CNVkit/cnvkit.sh'


pair_info = r'/data/stemcell/WES/GRCh38/stemcell_WES_sample_pair_220318.csv'
pair_info_tumor_col_name = 'Tumor'
pair_info_normal_col_name = 'Normal'


output_dir_suffix = '_CNVkit_result'
# output_dir_path = os.path.join(root_dir, output_dir_name)
qsub_log_dir_name = 'log_cnvkit'


##################### qsub 환경설정 ###################################

pbs_N = "cnvkit"
pbs_o = os.path.join(root_dir, qsub_log_dir_name)
pbs_j = "oe"
pbs_l_core = 5

######################################################################



if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)


pair_df = pd.read_csv(pair_info)


# print(pair_df)

pair_df.set_index(pair_info_tumor_col_name, inplace=True)
pair_dict = pair_df.to_dict('index') # {tumor : {normal:_ grade:_} dict 형태. fname

# print(pair_df)
# print(pair_dict)

# exit(0)

file_list = glob(os.path.join(root_dir, file_format))

# print(file_list)
# print(len(file_list))



for bam_file_path in file_list:
    print(bam_file_path)
    sample_name = bam_file_path.split(r'/')[-1].split(r'.')[0].split(r'_')[0]
    print(sample_name)

    
    output_dir_name = sample_name + output_dir_suffix
    output_dir_path = os.path.join(root_dir, output_dir_name)
    
    
    try:
        normal_sample_name = pair_dict[sample_name]['Normal']
    except KeyError:
        continue
    
    if os.path.isdir(output_dir_path) is False:
        os.mkdir(output_dir_path)
    
    normal_bam = normal_sample_name + '_sorted_deduped_recal.bam'
    normal_bam_path = os.path.join(root_dir, normal_bam)
    tumor_bam = bam_file_path
    
    out_ref_name = sample_name + '_refrence.cnn'
    out_ref_path = os.path.join(output_dir_path, out_ref_name)

    sp.call(f'echo "sh {sh_path} {tumor_bam} {normal_bam_path} {target} {ref_genome} {access} {out_ref_path} \
        {output_dir_path} {pbs_l_core}" | \
        qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)