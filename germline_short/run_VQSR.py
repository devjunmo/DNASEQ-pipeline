
# Gathering된 VCF에 대해 SNP/INDEL 모드로 각각 VQSR 과정 진행

import os
from glob import glob
import pandas as pd
import subprocess as sp


input_dir = r'/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/GVCF/genomic_DB/joint_call/gather'
input_vcf_name = r'stemcell_whole_samples.vcf.gz'
final_vcf_name = r'stemcell_whole_samples_applyVQSR.vcf.gz'
output_dir = os.path.join(input_dir, 'VQSR_out')
output_prefix = r'stemcell_WES'
interval_path = r'/data_244/refGenome/hg38/v0/interval_file/S07604514_Padded.bed'
ref_genome_ver = r'hg38'
ref_genome_path = r'/data_244/refGenome/hg38/GDC/GRCh38.d1.vd1.fa'
ref_genome_dir = r'/data_244/refGenome/hg38/v0' # known site 있는 dir

seq_type = r'WES'
var_type = r'SNP'

SRC_DIR = r'/data_244/src/ips_germ_210805/DNASEQ-pipeline/germline_short/'

input_vcf_path = os.path.join(input_dir, input_vcf_name)
output_prefix_path = os.path.join(output_dir, output_prefix)

if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)

if var_type == 'SNP':

    print('Run mode: SNP')
    
    # SNP - make recal table
    sp.call(f'nohup sh {SRC_DIR}VariantRecalibrator.sh {input_vcf_path} {output_prefix_path} \
        {ref_genome_path} {ref_genome_dir} {seq_type} {interval_path} {ref_genome_ver} {var_type}', shell=True)

    
    recal_table = output_prefix_path + r'.recal'
    tranch_file = output_prefix_path +  r'.tranches'
    output_VCF = os.path.join(output_dir, final_vcf_name)

    # SNP - apply VQSR
    sp.call(f'nohup sh {SRC_DIR}ApplyVQSR.sh {input_vcf_path} {recal_table} {tranch_file} {output_VCF} \
        {seq_type} {var_type} {interval_path} {ref_genome_path}', shell=True)
    
elif var_type == 'INDEL':
    
    print('Run mode: INDEL')
    exit(0)
    
    # # INDEL - make recal table
    # sp.call(f'nohup ')


    # # INDEL - apply VQSR
    # sp.call()

