import subprocess as sp
import glob
import natsort
import time
import sys
import getopt
import os


####################### hyper parameters ####################################################
# 디버깅모드시 실행파일은 주석처리, 중간생성물 지우기 여부는 False처리, max_looping=1 처리!!

THREADS = 16
# REF_GENOME_PATH = '/home/jun9485/data/refGenome/b37/human_g1k_v37.fasta' 

 # 중간 생성물 지우기 여부

# seq_type = "WES" # wes = interval file 요구됨 (알려진 exon 자리)
# INTERVAL_FILE_PATH = '/home/jun9485/data/refGenome/b37/SureSelect_v6_processed.bed'

max_looping = 50

##############################################################################################

gvcf_path = ''
read_name = ''
prefix = ''
INPUT_DIR = ''
REF_GENOME_PATH = ''
INTERVAL_FILE_PATH = ''
seq_type = ''

def rm_file(is_rm, file):
    if is_rm is True:
        os.remove(file)

def main(argv):
    file_name = argv[0]
    global bam_file
    global read_name
    global prefix
    global INPUT_DIR
    global REF_GENOME_PATH
    global INTERVAL_FILE_PATH
    global seq_type


    try:
        opts, etc_args = getopt.getopt(argv[1:], "hg:n:p:i:R:L:y:", ["help", "GVCF=", "readName=", "prefix=", "inputDir=, \
            -R {REF_GENOME_PATH} -L {INTERVAL_FILE_PATH} -y {seq_type}"])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(file_name, 'option error')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        print(opt)
        if opt in ("-h", "--help"):  # HELP 요청인 경우 사용법 출력
            print(file_name, 'file name..')
            sys.exit(0)
        elif opt in ("-g", "--GVCF"):
            read2 = arg
        elif opt in ("-n", "--readName"):
            read_name = arg
        elif opt in ("-p", "--prefix"):
            prefix = arg
        elif opt in ("-i", "--inputDir"):
            INPUT_DIR = arg
        elif opt in ("-R", "--ref"):
            REF_GENOME_PATH = arg
        elif opt in ("-L", "--interval"):
            INTERVAL_FILE_PATH = arg
        elif opt in ("-y", "--type"):
            seq_type = arg

main(sys.argv)

error_log_file = INPUT_DIR + "errorLog.txt"



# merge
gvcf_path_list = glob.glob(gvcf_path)
gvcf_path_list = natsort.natsorted(gvcf_path_list)

loop_count = 0

while True:
    try:
        mapping_time = time.time()
        err_msg = f'An_error_occurred_in_make_GVCF.sh:_Making_GVCF_file_was_failed.{read_name}'
        sp.check_call(fr'sh mappingBwaPE.sh {read1} {read2} {output_sam} {THREADS} {REF_GENOME_PATH} {read_name}', shell=True)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)

