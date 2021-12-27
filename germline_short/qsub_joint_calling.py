import subprocess as sp
import os
import pandas as pd
from glob import glob
import natsort


# 필요한 파일들 가져와서 qsub으로 넘기기 

####################### hyper parameters ########################################

# DB_DIR = r'/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/GVCF/genomic_DB'
DB_DIR = r'/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/GVCF/genomic_DB/re_chr2'
DB_NAME = r'stemcell_DB_chr*'

VCF_PREFIX = 'stemcell_jointCall_'
VCF_SUFFIX = '.vcf.gz'

db_snp_for_joint_call = r'/data_244/refGenome/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf'

OUTPUT_DIR_NAME = 'joint_call'
OUTPUT_DIR = os.path.join(DB_DIR, OUTPUT_DIR_NAME)

# INTERVAL_DIR = r'/data_244/refGenome/hg38/v0/interval_file/split_interval'
INTERVAL_DIR = r'/data_244/refGenome/hg38/v0/interval_file/split_interval/re_chr2'
INTERVAL_FORMAT = r'*.bed'

# hg 38
REF_GENOME_PATH = r'/data_244/refGenome/hg38/v0/gdc/GRCh38.d1.vd1.fa' # gdc

seq_type = "WES"

## pbs conifg
pbs_N = "stem.all.Jcall"
pbs_o = os.path.join(DB_DIR, r"pbs_jointCalling")
pbs_j = "oe"
pbs_l_core = 2

SRC_DIR = r"/data_244/src/ips_germ_210805/DNASEQ-pipeline/germline_short/"

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)

if os.path.isdir(OUTPUT_DIR) is False:
    os.mkdir(OUTPUT_DIR)

# interval file path lst가져와서 파일명 스플릿으로 chr 넘버 가져오고 
# DBdir 생성하기: stemcell_chr1, stemcell_chr2 .. 이런식으로..

# map 파일 생성..
# tmpdir 지정..
# thread 지정..



# print(natsort.natsorted(glob(os.path.join(DB_DIR, DB_NAME))))

# print(natsort.natsorted(glob(os.path.join(INTERVAL_DIR, INTERVAL_FORMAT))))

# exit(0)

db_lst = natsort.natsorted(glob(os.path.join(DB_DIR, DB_NAME)))
interval_file_lst = natsort.natsorted(glob(os.path.join(INTERVAL_DIR, INTERVAL_FORMAT)))

if len(db_lst) != len(interval_file_lst):
    print('DB list.len != interval file.len')
    exit(0)


for i in range(len(interval_file_lst)):
    interval_file = interval_file_lst[i]
    genomic_db = db_lst[i]
    print(interval_file)
    print(genomic_db)
    
    chr_info = interval_file.split(r'/')[-1].split(r'.')[0].split(r'_')[-1]
    
    vcf_name = VCF_PREFIX + chr_info + VCF_SUFFIX
    out_vcf_path = os.path.join(OUTPUT_DIR, vcf_name)
    tmp_dir_name = 'tmp_jointcall_' + chr_info
    jointcall_tmp_dir = os.path.join(OUTPUT_DIR, tmp_dir_name)
    # print(db_dir)
    # print(db_tmp_dir)
    # exit(0)
    
    # if os.path.isdir(db_dir) is False:
    #     os.mkdir(db_dir)
        
    if os.path.isdir(jointcall_tmp_dir) is False:
        os.mkdir(jointcall_tmp_dir)
    
    sp.call(f'echo "sh {SRC_DIR}joint_call.sh {REF_GENOME_PATH} {out_vcf_path} {db_snp_for_joint_call} {genomic_db} {jointcall_tmp_dir} {interval_file} {seq_type}" | \
        qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
    
    # exit(0)
    


# data_group_name = db_dir_name.split('_')[0]
# output_prefix = GVCF_DIR + data_group_name
# output_path = output_prefix + '.vcf.gz'

# sp.check_call(fr'nohup sh germline_short/joint_call.sh {REF_GENOME_PATH} {output_path} {db_snp_for_joint_call} {db_dir} {tmp_dir} {INTERVAL_FILE_PATH} {seq_type} &', shell=True)