import os
from glob import glob
import subprocess as sp


############## hyper params ##############

seq_type = 'WES'

input_dir = r'/data_244/utuc/'
input_format = r'recal_*.bam'


ref_dir = r'/data_244/refGenome/b37/'

ref_genome_path = ref_dir + 'human_g1k_v37.fasta'

interval_path = ref_dir + r'SureSelect_v6_processed.bed'

# select_type = 'SNP' # INDEL

snp_out_dir_name = r'snp/'

indel_out_dir_name = r'indel/'

snp_out_dir = input_dir + snp_out_dir_name
indel_out_dir = input_dir + indel_out_dir_name



if os.path.isdir(snp_out_dir) is False:
    os.mkdir(snp_out_dir)

if os.path.isdir(indel_out_dir) is False:
    os.mkdir(indel_out_dir)


############### pbs config ################

pbs_N = "utuc.mutect2.selectV"
pbs_o = input_dir + r"pbs_out/"
pbs_j = "oe"
pbs_l_core = 2
SRC_DIR = r"/data_244/src/utuc_pp/DNASEQ-pipeline/somatic_short/"

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)

###########################################



os.chdir(SRC_DIR)


input_lst = glob(input_dir + input_format)

for i in range(len(input_lst)):
    input_vcf = input_lst[i]
    f_name = input_vcf.split(r'/')[-1].split(r'.')[0]

    # snp

    sp.call

    # indel
