

import subprocess as sp
import os


input_dir = r'/data_244/WGS/HN00146173/recal_bam/'
ref_genome = r'/data_244/refGenome/b37/human_g1k_v37.fasta'
output_path = input_dir + 'sample.doc1'
input_bam_list_file = input_dir + 'bam_list.txt'
interval_file = r'/data_244/refGenome/b37/SureSelect_v6_processed.bed'


output_dir_name = r'maf/'
tmp_dir = input_dir + 'vcf/'
fasta_path = r'/data_240/refGenome/b37/human_g1k_v37.fasta'

qsub_type = 'pbs_pro' # 'pbs_pro' (최신, docker) / 'pbs_old' (240서버) 

seq_type = 'WGS'

####### pbs_pro config ###########
pbs_N = "mk_maf.WES"
pbs_o = input_dir + "qsub_log/"
pbs_j = "oe"
pbs_l_core = 4
##################################

####### pbs_old config ###########
qsub_config_file = r''
##################################



output_dir = input_dir + output_dir_name

if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


for i in range(len(input_lst)):

    f_name = input_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[-1] # teratoma-4
    f_type = input_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[-2] # snp/indel

    input_vcf_path = input_lst[i]
    output_maf_path = output_dir + f_type + '_' + f_name + '.maf'

    # sp.call(rf"perl vcf2maf.pl --input-vcf {input_vcf_path} --output-maf {output_maf_path} --ref-fasta {fasta_path} --tmp-dir {tmp_dir}", shell=True)

    if qsub_type == 'pbs_pro':
        
        if seq_type == 'WGS':
            sp.call(f'echo "gatk DepthOfCoverage -R {ref_genome} -O {output_path} -I {input_bam_list_file}" \
                    | qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l select={pbs_l_core} &', shell=True)
        
        elif seq_type == 'WES':
            sp.call(f'echo "gatk DepthOfCoverage -R {ref_genome} -O {output_path} -I {input_bam_list_file} -L {interval_file}" \
                    | qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l select={pbs_l_core} &', shell=True)
    
    elif qsub_type == 'pbs_old':
        
        if seq_type == 'WGS':
            sp.call(f'qsub {qsub_config_file} gatk DepthOfCoverage -R {ref_genome} -O {output_path} -I {input_bam_list_file} &', shell=True)
        
        elif seq_type == 'WES':
            sp.call(f'qsub {qsub_config_file} python germline_short/variant_calling_single_gs.py -b {bam_file} -n {read_name} -G {OUTPUT_GS_DIR} -R {REF_GENOME_PATH} -L {INTERVAL_FILE_PATH} -y {seq_type} &', shell=True)