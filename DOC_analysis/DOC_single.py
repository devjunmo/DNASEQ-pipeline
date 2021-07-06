
import subprocess as sp
import os


input_dir = r'/home/jun9485/data/WGS/HN00146173/recal_bam/'
ref_genome = r'/home/jun9485/data/refGenome/b37/human_g1k_v37.fasta'
output_path = input_dir + 'sample.doc1'
input_bam_list_file = input_dir + 'bam_list.txt'
interval_file = r'/home/jun9485/data/refGenome/b37/SureSelect_v6_processed.bed'


seq_type = 'WGS'


if seq_type == 'WGS':
    sp.call(f'gatk DepthOfCoverage -R {ref_genome} -O {output_path} -I {input_bam_list_file}', shell=True)

if seq_type == 'WES':
    sp.call(f'gatk DepthOfCoverage -R {ref_genome} -O {output_path} -I {input_bam_list_file} -L {interval_file}', shell=True)