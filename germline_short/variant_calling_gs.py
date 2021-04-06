import subprocess as sp
import glob
import natsort
import time
import sys
import getopt
import os



####################### hyper parameters ####################################################
# 디버깅모드시 실행파일은 주석처리, 중간생성물 지우기 여부는 False처리, max_looping=1 처리!!

consolidating_thread = 8
max_looping = 50

db_dir_name = r'HN00144124_DB/' # 이 형식 지켜줄것

db_snp_for_joint_call = r'/home/jun9485/data/refGenome/b37/dbsnp_138.b37.vcf'

tmp_dir_name = 'largeTmp'

##############################################################################################

GVCF_DIR = ''
REF_GENOME_PATH = ''
INTERVAL_FILE_PATH = ''
seq_type = ''

def rm_file(is_rm, file):
    if is_rm is True:
        os.remove(file)

def main(argv):
    file_name = argv[0]
    global GVCF_DIR
    global REF_GENOME_PATH
    global INTERVAL_FILE_PATH
    global seq_type


    try:
        opts, etc_args = getopt.getopt(argv[1:], "hg:R:L:y:", ["help", "GVCF=", "ref=", "interval=", "type="])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(file_name, 'option error')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        print(opt)
        if opt in ("-h", "--help"):  # HELP 요청인 경우 사용법 출력
            print(file_name, 'file name..')
            sys.exit(0)
        elif opt in ("-g", "--GVCF"):
            GVCF_DIR = arg
        elif opt in ("-R", "--ref"):
            REF_GENOME_PATH = arg
        elif opt in ("-L", "--interval"):
            INTERVAL_FILE_PATH = arg
        elif opt in ("-y", "--type"):
            seq_type = arg

main(sys.argv)

error_log_file = GVCF_DIR + "errorLog.txt"


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
gvcf_path_list = glob.glob(GVCF_DIR + '*.g.vcf.gz') 
gvcf_path_list = natsort.natsorted(gvcf_path_list)
read_list = []

for i in range(len(gvcf_path_list)):
    read_name = gvcf_path_list[i].split('.')[-4].split(r'/')[-1]
    read_list.append(read_name)

# merge
map_path = rf'{GVCF_DIR}' + 'mapFile.txt'
make_mapfile(read_list, gvcf_path_list, map_path)
print(read_list)
# exit(0)/
db_dir = GVCF_DIR + db_dir_name
batch_size = 50

os.makedirs(f'{GVCF_DIR}{tmp_dir_name}')
tmp_dir = GVCF_DIR + f'{tmp_dir_name}/'

loop_count = 0

while True:
    try:
        mapping_time = time.time()
        err_msg = f'An_error_occurred_in_consolidating_gvcfs.sh:_Consolidating_GVCF_files_was_failed.'
        sp.check_call(fr'nohup sh germline_short/consolidating_gvcfs.sh {db_dir} {batch_size} {INTERVAL_FILE_PATH} {map_path} {tmp_dir} {consolidating_thread} {seq_type} &', shell=True)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)



data_group_name = db_dir_name.split('_')[0]
output_prefix = GVCF_DIR + data_group_name
output_path = output_prefix + '.vcf.gz'

# joint call
while True:
    try:
        mapping_time = time.time()
        err_msg = f'An_error_occurred_in_joint_call.sh:_JointCalling_was_failed.'
        sp.check_call(fr'nohup sh germline_short/joint_call.sh {REF_GENOME_PATH} {output_path} {db_snp_for_joint_call} {db_dir} {tmp_dir} {INTERVAL_FILE_PATH} {seq_type} &', shell=True)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)


 # 