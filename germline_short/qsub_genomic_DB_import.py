import subprocess as sp
import os
import pandas as pd
from glob import glob
import natsort


# 필요한 파일들 가져와서 qsub으로 넘기기 

####################### hyper parameters ########################################

GVCF_DIR = r'/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/GVCF'   # 이 디렉토리에 계속 생성시킬것
OUTPUT_DIR_NAME = r'genomic_DB'

DB_PREFIX = r'stemcell_DB_'

OUTPUT_DIR = os.path.join(GVCF_DIR, OUTPUT_DIR_NAME)

INTERVAL_DIR = r'/data_244/refGenome/hg38/v0/interval_file/split_interval'
INTERVAL_FORMAT = r'*.bed'

# hg 38
REF_GENOME_PATH = r'/data_244/refGenome/hg38/v0/gdc/GRCh38.d1.vd1.fa' # gdc

# INTERVAL_FILE_PATH_DIR = '/data_244/refGenome/hg38/v0/interval_file/S07604514_Padded.bed'

batch_size = 50
thread = 3

seq_type = "WES"

## pbs conifg
pbs_N = "stem.all.gDB"
pbs_o = os.path.join(GVCF_DIR, r"pbs_mkDB")
pbs_j = "oe"
pbs_l_core = 3
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


def make_mapfile(_read_list, _gvcf_list, output_file_path):
    f = open(rf'{output_file_path}', mode='w')

    if len(_read_list) != len(_gvcf_list):
        print('\033[31m' + 'error: len(_read_list) != len(_gvcf_list)' + '\033[0m')
        exit(1)

    for i in range(len(_read_list)):
        data = f'{_read_list[i]}\t{_gvcf_list[i]}\n'
        f.write(data)
    f.close

# GVCF = r'\*.g.vcf.gz' # python인자로 넘길때 \* 필요
gvcf_path_list = glob(os.path.join(GVCF_DIR, '*.g.vcf.gz')) 
gvcf_path_list = natsort.natsorted(gvcf_path_list)
read_list = []


for i in range(len(gvcf_path_list)):
    read_name = gvcf_path_list[i].split('.')[-4].split(r'/')[-1]
    read_list.append(read_name)
print(read_list)
# merge
map_path = os.path.join(GVCF_DIR, 'mapFile.txt')
# make_mapfile(read_list, gvcf_path_list, map_path)

# exit(0)

# interval file

interval_file_lst = glob(os.path.join(INTERVAL_DIR, INTERVAL_FORMAT))


for i in range(len(interval_file_lst)):
    interval_file = interval_file_lst[i]
    print(interval_file)
    chr_info = interval_file.split(r'/')[-1].split(r'.')[0].split(r'_')[-1]
    
    db_name = DB_PREFIX + chr_info
    db_dir = os.path.join(OUTPUT_DIR, db_name)
    tmp_dir_name = 'tmp_' + chr_info
    db_tmp_dir = os.path.join(OUTPUT_DIR, tmp_dir_name)
    # print(db_dir)
    # print(db_tmp_dir)
    # exit(0)
    
    # if os.path.isdir(db_dir) is False:
    #     os.mkdir(db_dir)
        
    if os.path.isdir(db_tmp_dir) is False:
        os.mkdir(db_tmp_dir)
    
    sp.call(f'echo "sh {SRC_DIR}consolidating_gvcfs.sh {db_dir} {batch_size} {interval_file} {map_path} {db_tmp_dir} {thread} {seq_type}" | \
        qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
    

# db_dir = GVCF_DIR + db_dir_name
# batch_size = 50

# os.makedirs(f'{GVCF_DIR}{tmp_dir_name}')
# tmp_dir = GVCF_DIR + f'{tmp_dir_name}/'


# # sp.check_call(fr'nohup sh germline_short/consolidating_gvcfs.sh {db_dir} {batch_size} \
# #     {INTERVAL_FILE_PATH} {map_path} {tmp_dir} {consolidating_thread} {seq_type} &', shell=True)

# sp.call(f'echo "sh {SRC_DIR}germline_short/haplotypeCaller.sh {REF_GENOME_PATH} {output_gvcf} {bamfile} {INTERVAL_FILE_PATH} {seq_type} {hap_run_mode} {bamout_path}" | qsub \
#                         -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)