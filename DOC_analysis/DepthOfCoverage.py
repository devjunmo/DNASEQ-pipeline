

import subprocess as sp
import os
from glob import glob


# input_dir = r'/data_244/WGS/HN00146173/recal_bam/'
# ref_genome = r'/data_244/refGenome/b37/human_g1k_v37.fasta'
# output_path = input_dir + 'sample.doc1'
# input_bam_list_file = input_dir + 'bam_list.txt'
# interval_file = r'/data_244/refGenome/b37/SureSelect_v6_processed.bed'

input_dir = r'/data_244/utuc/'
input_format = r'*.bam'
ref_genome = r'/data_244/refGenome/b37/human_g1k_v37.fasta'
output_dir_name = 'DOC_results'
# output_path = input_dir + 'sample.doc1'
# input_bam_list_file = input_dir + 'bam_list.txt'

wgs_interval_file = r'/data_244/refGenome/b37/wgs_calling_regions.v1.list'
wes_interval_file = r'/data_244/refGenome/b37/SureSelect_v6_processed.bed'

qsub_type = 'pbs_pro' # 'pbs_pro' (최신, docker) / 'pbs_old' (240서버) / seq (큐섭 사용 x)

seq_type = 'WES'

if seq_type == 'WGS':
    interval_file = wgs_interval_file
elif seq_type == 'WES':
    interval_file = wes_interval_file
else:
    print('check interval file')
    exit(1)


####### pbs_pro config ###########
pbs_N = "UTUC.DOC.1"
pbs_o = input_dir + "qsub_log/"
pbs_j = "oe"
pbs_l_core = 2

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)
##################################

####### pbs_old config ###########
qsub_config_file = r'/home/jun9485/src/qsub.5'
##################################


input_path_lst = glob(input_dir + input_format)

output_dir = input_dir + output_dir_name + r'/'

if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


for i in range(len(input_path_lst)):

    f_name = input_path_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[-1] # teratoma-4
    # f_type = input_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[-2] # snp/indel

    input_bam_path = input_path_lst[i]
    output_path = output_dir + seq_type + '_' + f_name + '.doc'

    # sp.call(rf"perl vcf2maf.pl --input-vcf {input_vcf_path} --output-maf {output_maf_path} --ref-fasta {fasta_path} --tmp-dir {tmp_dir}", shell=True)

    if qsub_type == 'pbs_pro':
        sp.call(f'echo "gatk DepthOfCoverage -R {ref_genome} -O {output_path} -I {input_bam_path} -L {interval_file}" \
                | qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l select={pbs_l_core} &', shell=True)
    
    elif qsub_type == 'pbs_old':
        sp.call(f'qsub {qsub_config_file} gatk DepthOfCoverage -R {ref_genome} -O {output_path} -I {input_bam_path} -L {interval_file} &', shell=True)
    
    elif qsub_type == 'seq':
        sp.call(f'gatk DepthOfCoverage -R {ref_genome} -O {output_path} -I {input_bam_path} -L {interval_file}', shell=True)