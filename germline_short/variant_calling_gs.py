import subprocess as sp
import glob
import natsort
import time
import sys
import getopt
import os


####################### hyper parameters ####################################################
# 디버깅모드시 실행파일은 주석처리, 중간생성물 지우기 여부는 False처리, max_looping=1 처리!!

consolidating_thread = 16
max_looping = 50

db_dir_name = r'HN00144124_DB/'

##############################################################################################

gvcf_path = ''
read_list = ''
gvcf_list = ''
prefix_list = ''
INPUT_GS_DIR = ''
REF_GENOME_PATH = ''
INTERVAL_FILE_PATH = ''
seq_type = ''

def rm_file(is_rm, file):
    if is_rm is True:
        os.remove(file)

def main(argv):
    file_name = argv[0]
    global gvcf_path
    global read_list
    global gvcf_list
    global prefix_list
    global INPUT_GS_DIR
    global REF_GENOME_PATH
    global INTERVAL_FILE_PATH
    global seq_type


    try:
        opts, etc_args = getopt.getopt(argv[1:], "hg:r:v:p:i:R:L:y:", ["help", "GVCF=", "readList=", "gvcfList", "prefixList=", "inputDir=", \
            "ref=", "interval=", "type="])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(file_name, 'option error')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        print(opt)
        if opt in ("-h", "--help"):  # HELP 요청인 경우 사용법 출력
            print(file_name, 'file name..')
            sys.exit(0)
        elif opt in ("-g", "--GVCF"):
            gvcf_path = arg
        elif opt in ("-r", "--readList"):
            read_list = arg
        elif opt in ("-v", "--gvcfList"):
            gvcf_list = arg
        elif opt in ("-p", "--prefixList"):
            prefix_list = arg
        elif opt in ("-i", "--inputDir"):
            INPUT_GS_DIR = arg
        elif opt in ("-R", "--ref"):
            REF_GENOME_PATH = arg
        elif opt in ("-L", "--interval"):
            INTERVAL_FILE_PATH = arg
        elif opt in ("-y", "--type"):
            seq_type = arg

main(sys.argv)

error_log_file = INPUT_GS_DIR + "errorLog.txt"


def make_mapfile(_read_list, _gvcf_list, output_file_path):
    f = open(rf'{output_file_path}', mode='w')

    if len(_read_list) != len(_gvcf_list):
        print('\033[31m' + 'error: len(_read_list) != len(_gvcf_list)' + '\033[0m')
        exit(1)

    for i in range(len(_read_list)):
        data = f'{_read_list[i]}\t{_gvcf_list[i]}\n'
        f.write(data)
    f.close



# merge
map_path = rf'{INPUT_GS_DIR} + mapFile.txt'
make_mapfile(read_list, gvcf_list, map_path)

db_dir = INPUT_GS_DIR + db_dir_name
batch_size = 50

tmp_dir = INPUT_GS_DIR + 'largeTmp/'

loop_count = 0

while True:
    try:
        mapping_time = time.time()
        err_msg = f'An_error_occurred_in_consolidating_gvcfs.sh:_Consolidating_GVCF_files_was_failed.'
        sp.check_call(fr'sh consolidating_gvcfs.sh {db_dir} {batch_size} {INTERVAL_FILE_PATH} {map_path} {tmp_dir} {consolidating_thread} {seq_type}', shell=True)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)

