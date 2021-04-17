import subprocess as sp
import glob
import natsort
import time
import sys
import getopt
import os



####################### hyper parameters ####################################################
# 디버깅모드시 실행파일은 주석처리, 중간생성물 지우기 여부는 False처리, max_looping=1 처리!!

max_looping = 1

## HaplotypeCaller(hc) / CNNVariantScore(cnn) /FilterVariantTranches ~ Funcotator(ft) / 
gs_work_type = 'ft'

CNN_model = '2D'

REF_DIR = r'/home/jun9485/data/refGenome/b37/'

data_source_dir = r'/home/jun9485/data/funcotator_data_source/funcotator_dataSources.v1.7.20200521g'

##############################################################################################

BAM_FILE = ''
READ_NAME = ''
GS_DIR = ''
REF_GENOME_PATH = ''
INTERVAL_FILE_PATH = ''
seq_type = ''

def rm_file(is_rm, file):
    if is_rm is True:
        try:
            os.remove(file)
        except FileNotFoundError:
            print(f'{file} 파일이 존재하지 않아 삭제하지 못함')


def main(argv):
    file_name = argv[0]
    global BAM_FILE
    global READ_NAME
    global GS_DIR
    global REF_GENOME_PATH
    global INTERVAL_FILE_PATH
    global seq_type


    try:
        opts, etc_args = getopt.getopt(argv[1:], "hb:n:G:R:L:y:", ["help", "BAM=", "NAME=", "GSDIR=", "ref=", "interval=", "type="])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(file_name, 'option error')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        print(opt)
        if opt in ("-h", "--help"):  # HELP 요청인 경우 사용법 출력
            print(file_name, 'file name..')
            sys.exit(0)
        elif opt in ("-b", "--BAM"):
            BAM_FILE = arg
        elif opt in ("-n", "--NAME"):
            READ_NAME = arg
        elif opt in ("-G", "--GSDIR"):
            GS_DIR = arg
        elif opt in ("-R", "--ref"):
            REF_GENOME_PATH = arg
        elif opt in ("-L", "--interval"):
            INTERVAL_FILE_PATH = arg
        elif opt in ("-y", "--type"):
            seq_type = arg

main(sys.argv)

error_log_file = GS_DIR + "errorLog.txt"



# if gs_work_type == 'hc':
#     # HaplotypeCaller 실행 <- .244서버에서 docker로 CNN돌려야 해서 부득이하게 분리
#     if is_using_qsub is True:
#         sp.call(f'qsub {qsub_config_name} sh germline_short/haplotypeCaller.sh {REF_GENOME_PATH} {output_raw_vcf} {bam_file} {INTERVAL_FILE_PATH} {seq_type} {haplotype_caller_mode}', shell=True)
#     elif is_using_qsub is False:
#         exit(0)
# elif gs_work_type == 'ft':
#     if is_using_qsub is True:
#         sp.call(f'qsub {qsub_config_name} sh germline_short/filter_variant_tranches.sh {} {} {} {} {}', shell=True)
#     elif is_using_qsub is False:
#         exit(0)


raw_vcf = READ_NAME + '.vcf.gz'
output_raw_vcf = GS_DIR + raw_vcf

if gs_work_type == 'hc':
    loop_count = 0
    haplotype_caller_mode = 'single'
    while True:
        try:
            mapping_time = time.time()
            err_msg = f'An_error_occurred_in_haplotypeCaller.sh:_making_a_raw_vcf_file_was_failed.'
            sp.check_call(fr'sh germline_short/haplotypeCaller.sh {REF_GENOME_PATH} {output_raw_vcf} {BAM_FILE} {INTERVAL_FILE_PATH} {seq_type} {haplotype_caller_mode}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)

scored_prefix = 'scored_'
output_scored_vcf = GS_DIR + scored_prefix + READ_NAME + '.vcf'

filterd_prefix = 'filtered_'
output_filtered_scored_vcf = GS_DIR + filterd_prefix + scored_prefix + READ_NAME + '.vcf'



if gs_work_type == 'ft':
    loop_count = 0

    while True:
        try:
            mapping_time = time.time()
            err_msg = f'An_error_occurred_in_filter_variant_tranches.sh:_Filtering_VCF_files_was_failed.'
            sp.check_call(fr'sh germline_short/filter_variant_tranches.sh {output_scored_vcf} {output_filtered_scored_vcf} {INTERVAL_FILE_PATH} {CNN_model} {seq_type} {REF_DIR}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)

exit(0)

# if gs_work_type == 'ft':
#     loop_count = 0

#     while True:
#         try:
#             mapping_time = time.time()
#             err_msg = f'An_error_occurred_in_consolidating_gvcfs.sh:_Consolidating_GVCF_files_was_failed.'
#             sp.check_call(fr'sh germline_short/funcotator.sh {}', shell=True)
#             break

#         except sp.CalledProcessError as e:
#             sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
#             loop_count += 1
#             if loop_count > max_looping:
#                 exit(0)