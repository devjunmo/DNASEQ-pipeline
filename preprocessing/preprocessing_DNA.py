import subprocess as sp
import glob
import natsort
import time
import sys
import getopt
import os


####################### hyper parameters ####################################################
# 디버깅모드시 실행파일은 주석처리, 중간생성물 지우기 여부는 False처리, max_looping=1 처리!!

# !!!! 중요: make_recal_table.sh의 hyper parameters도 설정해줘야 함 !!!!

THREADS = 16                                        
REF_GENOME_DIR = '/home/jun9485/data/refGenome/b37/'

 # 중간 생성물 지우기 여부
rm_sam = True
rm_raw_bam = True
rm_sorted_bam = True
rm_dedup_sorted_bam = True

sorting_order = 'coordinate' # or queryname

max_looping = 50

##############################################################################################

read1 = ''
read2 = ''
read_name = ''
prefix = ''
INPUT_DIR = ''
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
    global read1
    global read2
    global read_name
    global prefix
    global INPUT_DIR
    global REF_GENOME_PATH
    global INTERVAL_FILE_PATH
    global seq_type

    try:
        opts, etc_args = getopt.getopt(argv[1:], "ha:b:n:p:i:R:L:y:", ["help", "readA=", "readB=", "readName=", "prefix=", "inputDir=",\
            "ref=", "interval=", "type="])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(file_name, 'option error')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        print(opt)
        if opt in ("-h", "--help"):  # HELP 요청인 경우 사용법 출력
            print(file_name, 'file name..')
            sys.exit(0)

        elif opt in ("-a", "--readA"):  # 인스턴명 입력인 경우
            read1 = arg
        elif opt in ("-b", "--readB"):
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



# mapping
output_sam = prefix + '.sam' 

loop_count = 0

while True:
    try:
        mapping_time = time.time()
        err_msg = f'An_error_occurred_in_mappingBwaPE.sh:_Mapping_reads_was_failed.{read_name}'
        sp.check_call(fr'sh preprocessing/mappingBwaPE.sh {read1} {read2} {output_sam} {THREADS} {REF_GENOME_PATH} {read_name}', shell=True)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)



# sam -> bam
output_bam = prefix + '.bam'

loop_count = 0

while True:
    try:
        s2b_time = time.time()
        err_msg = f'An_error_occurred_in_sam2bam.sh:_Converting_SAM_to_BAM_was_failed._{read_name}'
        sp.check_call(fr'sh preprocessing/sam2bam.sh {output_sam} {output_bam} {THREADS}', shell=True)
        rm_file(rm_sam, output_sam) # sam 삭제 여부
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)



# sorting bam -> sorting_order: coordinate (-n 주면 queryname)
sort_suffix = 'sorted_' + read_name + '.bam'
sorted_bam = INPUT_DIR + sort_suffix

loop_count = 0

while True:
    try:
        sorting_time = time.time()
        err_msg = f'An_error_occurred_in_sortingBam.sh:_Sorting_the_BAM_file_was_failed._{read_name}'
        sp.check_call(fr'sh preprocessing/sortingBam.sh {output_bam} {sorted_bam} {THREADS} {read_name}', shell=True)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)



# dedup bam
metric_prefix = INPUT_DIR + read_name + '_'
dedup_suffix = 'deduped_' + sort_suffix
dedup_sorted_bam = INPUT_DIR + dedup_suffix

loop_count = 0

while True:
    try:
        dedup_time = time.time()
        err_msg = f'An_error_occurred_in_deduplicateBam.sh:_Deduplicating_the_BAM_file_was_failed._{read_name}'
        sp.check_call(fr'sh preprocessing/deduplicateBam.sh {sorted_bam} {dedup_sorted_bam} {sorting_order} {metric_prefix}', shell=True)
        rm_file(rm_sorted_bam, sorted_bam) # sorted bam 삭제
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)



# indexing_dedupBam

loop_count = 0

while True:
    try:
        dedup_time = time.time()
        err_msg = f'An_error_occurred_in_indexing_dedup_bam.sh:_Indexing_the_BAM_file_was_failed._{read_name}'
        sp.check_call(fr'sh preprocessing/indexing_dedup_bam.sh {THREADS} {dedup_sorted_bam}', shell=True)
        rm_file(rm_raw_bam, output_bam) # raw bam 삭제
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)



# making recal_table
table_path = INPUT_DIR + read_name + '_recal.table'
ram_to_use = 20

loop_count = 0

while True:
    try:
        mk_table_time = time.time()
        err_msg = f'An_error_occurred_in_make_recal_table.sh:_Making_a_recal.table_file_was_failed._{read_name}'
        sp.check_call(fr'sh preprocessing/make_recal_table.sh {dedup_sorted_bam} {table_path} {REF_GENOME_PATH} {REF_GENOME_DIR} {seq_type} {INTERVAL_FILE_PATH}', shell=True)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)



# applying the recal_table
recal_suffix = 'recal_' + dedup_suffix
recal_dedup_sorted_bam = INPUT_DIR + recal_suffix
ram_to_use = 20

loop_count = 0

while True:
    try:
        mk_table_time = time.time()
        err_msg = f'An_error_occurred_in_applyBQSR.sh:_Applying_the_recalTable_to_the_BAM_file_was_failed._{read_name}'
        sp.check_call(fr'sh preprocessing/applyBQSR.sh {dedup_sorted_bam} {recal_dedup_sorted_bam} {table_path} {REF_GENOME_PATH} {seq_type} {INTERVAL_FILE_PATH}', shell=True)
        rm_file(rm_dedup_sorted_bam, dedup_sorted_bam)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)



