import os
from glob import glob
import subprocess as sp


input_dir = r'/data_240/WES/teratoma_annotation/teratoma_sample/'
input_format = r'hardFiltered_*_Teratoma*.vcf'
output_dir_name = r'maf/'
tmp_dir = input_dir + 'vcf/'
fasta_path = r'/data_240/refGenome/b37/human_g1k_v37.fasta'

output_dir = input_dir + output_dir_name

if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)

if os.path.isdir(tmp_dir) is False:
    os.mkdir(tmp_dir)

input_lst = glob(input_dir + input_format)

os.chdir(r'/root/mskcc-vcf2maf-2235eed')

for i in range(len(input_lst)):

    f_name = input_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[-1] # teratoma-4
    f_type = input_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[-2] # snp/indel
    
    input_vcf_path = input_lst[i]
    output_maf_path = output_dir + f_type + '_' + f_name + '.maf' 

    sp.call(rf"perl vcf2maf.pl --input-vcf {input_vcf_path} --output-maf {output_maf_path} --ref-fasta {fasta_path} --tmp-dir {tmp_dir}", shell=True)


    # tumor-id 부분 넣어줘서 다시코딩