import subprocess as sp
import sys
import getopt
import os



####################### hyper parameters ####################################################

# script_dir = '/data_244/src/utuc_pp/DNASEQ-pipeline/preprocessing/'

SRC_DIR = r"/data_244/src/ips_germ_210805/DNASEQ-pipeline/somatic_short/"
os.chdir(SRC_DIR) # 문제 발생시 넣는 코드

##############################################################################################



normal_name = ''
tumor_name = ''
INPUT_DIR = ''
REF_GENOME_PATH = ''
INTERVAL_FILE_PATH = ''
seq_type = ''
PON_PATH = ''
SEC_PATH = ''
GERM_SRC_PATH = ''
OUTPUT_DIR = ''


def rm_file(is_rm, file):
    if is_rm is True:
        try:
            os.remove(file)
        except FileNotFoundError:
            print(f'{file} 파일이 존재하지 않아 삭제하지 못함')


def main(argv):
    file_name = argv[0]
    global normal_name
    global tumor_name
    global INPUT_DIR
    global REF_GENOME_PATH
    global INTERVAL_FILE_PATH
    global seq_type
    global PON_PATH
    global SEC_PATH
    global GERM_SRC_PATH
    global OUTPUT_DIR

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hn:t:I:R:L:P:S:G:y:O:", ["help", "normalName=", "tumorName=", "inputDir=", "refPath=", "interval=", \
            "pon", "sec", "germSrc", "seqType=", "outputDir="])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(file_name, 'option error')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        print(opt)
        if opt in ("-h", "--help"):  # HELP 요청인 경우 사용법 출력
            print(file_name, 'file name..')
            sys.exit(0)

        elif opt in ("-n", "--normalName"):  # 인스턴명 입력인 경우
            normal_name = arg
        elif opt in ("-t", "--tumorName"):
            tumor_name = arg
        elif opt in ("-I", "--inputDir"):
            INPUT_DIR = arg
        elif opt in ("-R", "--refPath"):
            REF_GENOME_PATH = arg
        elif opt in ("-L", "--interval"):
            INTERVAL_FILE_PATH = arg
        elif opt in ("-P", "--pon"):
            PON_PATH = arg
        elif opt in ("-S", "--sec"):
            SEC_PATH = arg
        elif opt in ("-G", "--germSrc"):
            GERM_SRC_PATH = arg
        elif opt in ("-y", "--seqType"):
            seq_type = arg
        elif opt in ("-O", "--outputDir"):
            OUTPUT_DIR = arg


main(sys.argv)


    
# Mutect2

# # [Tumor bam path] [Normal bam path] [Normal name] [Germline src] [Ref genome] [interval] [Output prefix] [PON] [seq_type]

tumor_bam = INPUT_DIR + 'recal_deduped_sorted_' + tumor_name + '.bam'
normal_bam = INPUT_DIR + 'recal_deduped_sorted_' + normal_name + '.bam'
# tumor_bam = INPUT_DIR + tumor_name + '_sorted_dedup_recal.bam'
# normal_bam = INPUT_DIR + normal_name + '_sorted_dedup_recal.bam'

output_prefix = OUTPUT_DIR + tumor_name

sp.call(rf'sh ./mutect2.sh {tumor_bam} {normal_bam} {normal_name} {GERM_SRC_PATH} {REF_GENOME_PATH} \
                        {INTERVAL_FILE_PATH} {output_prefix} {PON_PATH} {seq_type}', shell = True)


# LearnReadOrientationModel

in_f1r2 = output_prefix + r'.f1r2.tar.gz'
out_rom = output_prefix + r'.rom.tar.gz'

sp.call(rf'sh ./learnReadOrientationModel.sh {in_f1r2} {out_rom}', shell = True)


# GetPileupSummaries

out_gp_table = output_prefix + r'.getpileupsummaries.table'

sp.call(rf'sh ./getPileupSummaries.sh {tumor_bam} {SEC_PATH} {out_gp_table}', shell=True)


# CalculateContamination

out_seg_table = output_prefix + r'.segments.table'
out_contam_table = output_prefix + r'.calculatecontamination.table'

sp.call(rf'sh ./calculateContamination.sh {out_gp_table} {out_seg_table} {out_contam_table}', shell=True)


# FilterMutectCalls
# [input.mutectl.vcf] [output.mutect.filtered.vcf] [ref genome] [i.segment.table] [i.calculatecontamination.table] [i.rom.tar.gz]

in_mutect_vcf = output_prefix + r'_mutect2.vcf'
output_filtered_vcf = OUTPUT_DIR + r'filtered_' + tumor_name + r'_mutect2.vcf'
# output_filtered_vcf = OUTPUT_DIR  + tumor_name + r'_mutect2_filtered.vcf'

sp.call(rf'sh ./filterMutectCalls.sh {in_mutect_vcf} {output_filtered_vcf} {REF_GENOME_PATH} \
                {out_seg_table} {out_contam_table} {out_rom}', shell = True)