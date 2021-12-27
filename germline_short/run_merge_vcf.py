
from glob import glob
import os
import subprocess as sp
import natsort


input_dir = r'/data_244/stemcell/WES/hardfilterd_vcf/dp_apply'

input_snp_format = r'hardFiltered_SNP*.gz'
input_indel_format = r'hardFiltered_INDEL*.gz'

out_dir = os.path.join(input_dir, 'merged_vcf')
output_suffix = r'_HAP_filtered.vcf.gz'

src_path = r'/data_244/src/ips_germ_210805/DNASEQ-pipeline/germline_short/merge_SNP_INDEL.sh'


if os.path.isdir(out_dir) is False:
    os.mkdir(out_dir)


snp_path_lst = natsort.natsorted(glob(os.path.join(input_dir, input_snp_format)))
indel_path_lst = natsort.natsorted(glob(os.path.join(input_dir, input_indel_format)))



# print(snp_path_lst)
# print(indel_path_lst)

print(os.getcwd())

if len(snp_path_lst) != len(indel_path_lst):
    print('snp.len != indel.len')
    exit(1)


for i in range(len(snp_path_lst)):

    snp_path = snp_path_lst[i]
    indel_path = indel_path_lst[i]

    # 추후 수정

    sample_name = snp_path.split(r'/')[-1].split(r'.')[0].split(r'_')[-1]
    print(sample_name)
    out_maf_name = sample_name + output_suffix
    
    output_path = os.path.join(out_dir, out_maf_name)
    
    sp.call(rf'sh {src_path} {snp_path} {indel_path} {output_path}', shell=True) #  [snp_vcf] [indel_vcf] [output_path]