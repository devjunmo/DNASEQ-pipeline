import os
from glob import glob
import subprocess as sp
import pandas as pd


input_dir = r'/data_244/utuc/utuc_gdc_2nd_LG2_re/mutect2_utuc/maf/'

input_format = r'*_pass.vcf'

output_dir_name = r'maf/'
tmp_dir = input_dir + r'vep_vcfs/'
# fasta_path = r'/data_244/refGenome/b37/human_g1k_v37.fasta'
fasta_path = r'/data_244/refGenome/hg38/v0/gdc/GRCh38.d1.vd1.fa'

SRC_DIR = r"/home/pbsuser/mskcc-vcf2maf-754d68a/"
SRC_PATH = SRC_DIR + "vcf2maf.pl"

run_type = r'qsub' # qsub, single

ref_ver = 'GRCh38' # GRCh37 


## pbs config
pbs_N = "utuc.gdc.2rd2.annot"
pbs_o = input_dir + r"qsub_log/"
pbs_j = "oe"
pbs_l_core = 4


output_dir = input_dir + output_dir_name

tumor_normal_id_info = r'/data_244/utuc/utuc_NT_pair_ver_211029_utuc4_1.csv'


pair_df = pd.read_csv(tumor_normal_id_info)
# print(pair_df)

pair_df.set_index('Tumor', inplace=True)

pair_dict = pair_df.to_dict('index') # {tumor : {normal:_ grade:_} dict 형태. fname

print(pair_dict)

# exit(0)




if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)

if os.path.isdir(tmp_dir) is False:
    os.mkdir(tmp_dir)

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)


input_lst = glob(input_dir + input_format)

# print(input_lst)
# print(len(input_lst))
# exit(0)

# os.chdir(r'/root/mskcc-vcf2maf-2235eed')

for i in range(len(input_lst)):

    sample_name = input_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[0] # 20S-31099-A4-5
    
    # break

    # t_id = sample_name.split('-')[-2] + '-' + sample_name.split('-')[-1] # A4-5
    t_id = sample_name

    try:
        n_id = pair_dict[sample_name]['Normal']

    except KeyError as e:
        print(f'{sample_name} does not have target normal sample')
        continue

    caller_name = input_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[1] # mutect2
    
    input_vcf_path = input_lst[i]
    output_maf_path = output_dir + sample_name + '_' + caller_name + '.maf' 

    # print(input_vcf_path)
    # print(output_maf_path)
    # break

    # sp.call(rf"perl vcf2maf.pl --input-vcf {input_vcf_path} --output-maf {output_maf_path} --ref-fasta {fasta_path} --tmp-dir {tmp_dir}", shell=True)

    if run_type == 'qsub':
        sp.call(f'echo "perl {SRC_PATH} --input-vcf {input_vcf_path} --output-maf {output_maf_path} --ref-fasta {fasta_path} --tmp-dir {tmp_dir} \
                    --tumor-id {sample_name} --normal-id {n_id} --vcf-tumor-id {t_id} --vcf-normal-id {n_id} --ncbi-build {ref_ver}" \
                | qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
    elif run_type == 'single':
        sp.call(f'perl {SRC_PATH} --input-vcf {input_vcf_path} --output-maf {output_maf_path} --ref-fasta {fasta_path} --tmp-dir {tmp_dir} \
                    --tumor-id {sample_name} --normal-id {n_id} --vcf-tumor-id {t_id} --vcf-normal-id {n_id} --ncbi-build {ref_ver}', shell=True)



