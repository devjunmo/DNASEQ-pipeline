import subprocess as sp
import glob
import natsort
import time
from time import sleep
import os


# hard filtered 파일 리스트 가져와서
# name list 따고
# 돌리는데, 큐섭으로 돌리기가 일단은 불가능. 도커에 아직 큐섭 안깔음.

##################### HYPER PARAMETERS ############################

working_dir = r'/root/mskcc-vcf2maf-2235eed'

input_dir = r'/data_240/WES/germline_21_24/gs/'
output_dir = r'/data_240/WES/germline_21_24/gs/maf_files/'

###################################################################




os.chdir(working_dir)

input_VCF_list = glob.glob(input_dir + 'hardFiltered_*.vcf')
input_VCF_list = natsort.natsorted(input_VCF_list)

vcf_list_len = len(input_VCF_list)

print("input len =", vcf_list_len)
print(input_VCF_list)

exit(0)


for i in range(vcf_list_len):
    input_vcf = input_VCF_list[i]
    vcf_name = input_vcf.split('.')[-2].split(r'/')[-1].split(r'_')[-1] # Teratoma-13
    type_name = input_vcf.split('.')[-2].split(r'/')[-1].split(r'_')[-2] # INDEL
    output_path =  output_dir + vcf_name + '_' + type_name + '.maf'

    sp.call(rf'perl vcf2maf.pl --input-vcf {input_vcf} --output-maf {output_path} --tumor-id {vcf_name}', shell=True)