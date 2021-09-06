
import subprocess as sp
import glob
import natsort
import time
import sys
import getopt
import os



####################### hyper parameters ####################################################
# 디버깅모드시 실행파일은 주석처리, 중간생성물 지우기 여부는 False처리, max_looping=1 처리!!

max_looping = 0

script_dir = r"/data_244/src/ips_germ_210805/DNASEQ-pipeline/germline_short/"

## WORK TYPE ##
## case 1. haplotypeCaller ~ hardFilter (hard)
## case 2. filter된 cnn scored vcf를 indel과 snp로 나눌때 (spcnn)
## case 3. HaplotypeCaller(hc) / CNNVariantScore(cnn) /FilterVariantTranches ~ Funcotator(ft) / -> 사용 x
## case 4. hard filter된 vcf를 CNNVariantScore ~ FilterVariantTranches까지 진행할 때 (hardcnn)

gs_work_type = 'hard'

CNN_model = '2D'

REF_DIR = r'/data_244/refGenome/hg38/v0/'

data_source_dir = r'/home/jun9485/data/funcotator_data_source/funcotator_dataSources.v1.7.20200521g'

##############################################################################################

os.chdir(script_dir) # 문제 발생시 넣는 코드

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


vcf_gz = '.vcf.gz'

raw_vcf = READ_NAME + vcf_gz
output_raw_vcf = GS_DIR + raw_vcf


if gs_work_type == 'hard':

    loop_count = 0
    haplotype_caller_mode = 'single'
    while True:
        try:
            err_msg = f'An_error_occurred_in_haplotypeCaller.sh:_making_a_raw_vcf_file_was_failed.'
            sp.check_call(fr'sh ./haplotypeCaller.sh {REF_GENOME_PATH} {output_raw_vcf} {BAM_FILE} {INTERVAL_FILE_PATH} {seq_type} {haplotype_caller_mode}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh ./write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)



    snp_type = 'SNP'
    indel_type = 'INDEL'

    snp_vcf = READ_NAME + '_' + snp_type
    indel_vcf = READ_NAME + '_' + indel_type

    snp_vcf_path = GS_DIR + snp_vcf + vcf_gz
    indel_vcf_path = GS_DIR + indel_vcf + vcf_gz

    hardFilterd_suffix = 'hardFiltered'

    snp_hard = snp_vcf + '_' + hardFilterd_suffix
    indel_hard = indel_vcf + '_' + hardFilterd_suffix

    snp_hardFiltered_output = GS_DIR + snp_hard + vcf_gz
    indel_hardFiltered_output = GS_DIR + indel_hard + vcf_gz
    


    # SelectVariants - snps
    loop_count = 0
    while True:
        try:
            err_msg = f'An_error_occurred_in_SelectVariants.sh:_making_a_SNP_vcf_file_was_failed.'
            sp.check_call(fr'sh ./select_variants.sh {REF_GENOME_PATH} {output_raw_vcf} {snp_vcf_path} {snp_type} {seq_type} {INTERVAL_FILE_PATH}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh ./write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)
    


    # VariantFilteration - snp filtering
    loop_count = 0
    while True:
        try:
            err_msg = f'An_error_occurred_in_variant_filteration.sh:_making_a_SNP_filtered_vcf_file_was_failed.'
            sp.check_call(fr'sh ./variant_filteration.sh {snp_vcf_path} {snp_hardFiltered_output} {snp_type} {seq_type} {INTERVAL_FILE_PATH}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh ./write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)



    # SelectVariants - indels
    loop_count = 0
    while True:
        try:
            err_msg = f'An_error_occurred_in_SelectVariants.sh:_making_a_INDEL_vcf_file_was_failed.'
            sp.check_call(fr'sh ./select_variants.sh {REF_GENOME_PATH} {output_raw_vcf} {indel_vcf_path} {indel_type} {seq_type} {INTERVAL_FILE_PATH}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh ./write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)
    

    # VariantFilteration - indel filtering
    loop_count = 0
    while True:
        try:
            err_msg = f'An_error_occurred_in_variant_filteration.sh:_making_a_INDEL_filtered_vcf_file_was_failed.'
            sp.check_call(fr'sh ./variant_filteration.sh {indel_vcf_path} {indel_hardFiltered_output} {indel_type} {seq_type} {INTERVAL_FILE_PATH}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh ./write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)



    merge_output_dir = os.path.join(GS_DIR, 'merged_VCF')

    if os.path.isdir(merge_output_dir) is False:
        os.mkdir(merge_output_dir)
    
    merge_output_name = READ_NAME + '_' + hardFilterd_suffix + '_germline_merged' + vcf_gz

    merge_path = os.path.join(merge_output_dir, merge_output_name)



    # Merge VCF (SNP + INDEL)

    loop_count = 0
    while True:
        try:
            err_msg = f'An_error_occurred_in_merge_SNP_INDEL.sh:_merging_files_was_failed.'
            sp.check_call(fr'sh ./merge_SNP_INDEL.sh {snp_hardFiltered_output} {indel_hardFiltered_output} {merge_path}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh ./write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)
















if gs_work_type == 'spcnn':

    filtered_scored_vcf_name = 'filtered_scored_' + READ_NAME + '.vcf.gz'
    filtered_scored_vcf_path = GS_DIR + filtered_scored_vcf_name

    snp_type = 'SNP'
    indel_type = 'INDEL'

    snp_vcf = GS_DIR + snp_type + '_' + 'cnn_' + READ_NAME + '.vcf.gz'
    indel_vcf = GS_DIR + indel_type + '_' + 'cnn_' + READ_NAME + '.vcf.gz'


    # SelectVariants - snps
    loop_count = 0
    while True:
        try:
            err_msg = f'An_error_occurred_in_SelectVariants.sh:_making_a_SNP_vcf_file_was_failed.'
            sp.check_call(fr'sh germline_short/select_variants.sh {REF_GENOME_PATH} {filtered_scored_vcf_path} {snp_vcf} {snp_type} {seq_type} {INTERVAL_FILE_PATH}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)
    
    # SelectVariants - indels
    loop_count = 0
    while True:
        try:
            err_msg = f'An_error_occurred_in_SelectVariants.sh:_making_a_INDEL_vcf_file_was_failed.'
            sp.check_call(fr'sh germline_short/select_variants.sh {REF_GENOME_PATH} {filtered_scored_vcf_path} {indel_vcf} {indel_type} {seq_type} {INTERVAL_FILE_PATH}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)




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



if gs_work_type == 'hardcnn':

    VCF_SFX = '.vcf.gz'

    # snp

    HARD_PFX_SNP = 'hardFiltered_SNP_'
    
    input_hard_vcf_path_snp = GS_DIR + HARD_PFX_SNP + READ_NAME + VCF_SFX

    b_name = BAM_FILE.split(r'/')[-1].split(r'.')[0].split(r'_')[-1]
    v_name = input_hard_vcf_path_snp.split(r'/')[-1].split(r'.')[-3].split(r'_')[-1]

    if b_name != v_name:
        print('BAMfile, VCFfile do not matched.')
        exit(1)
    
    scored_prefix = 'scored_'
    scored_hard_vcf_path_snp = GS_DIR + scored_prefix + HARD_PFX_SNP + READ_NAME + VCF_SFX

    # CNNScoreVariants 실행
    sp.call(f'sh germline_short/cnn_score_variants.sh {BAM_FILE} {input_hard_vcf_path_snp} {REF_GENOME_PATH} {scored_hard_vcf_path_snp} {INTERVAL_FILE_PATH} {CNN_model} {seq_type}', shell=True)

    filter_prefix = 'cnnFiltered_'
    cnn_filtered_path_snp = GS_DIR + filter_prefix + scored_prefix + HARD_PFX_SNP + READ_NAME + VCF_SFX

    # FilterVariantTranches 실행
    sp.call(f'sh germline_short/filter_variant_tranches.sh {scored_hard_vcf_path_snp} {cnn_filtered_path_snp} {INTERVAL_FILE_PATH} {CNN_model} {seq_type}', shell=True)


    # indel
    HARD_PFX_INDEL = 'hardFiltered_INDEL_'

    input_hard_vcf_path_indel = GS_DIR + HARD_PFX_INDEL + READ_NAME + VCF_SFX
    scored_hard_vcf_path_indel = GS_DIR + scored_prefix + HARD_PFX_INDEL + READ_NAME + VCF_SFX

    # CNNScoreVariants 실행
    sp.call(f'sh germline_short/cnn_score_variants.sh {BAM_FILE} {input_hard_vcf_path_indel} {REF_GENOME_PATH} {scored_hard_vcf_path_indel} {INTERVAL_FILE_PATH} {CNN_model} {seq_type}', shell=True)
    
    cnn_filtered_path_indel = GS_DIR + filter_prefix + scored_prefix + HARD_PFX_INDEL + READ_NAME + VCF_SFX
    
    # FilterVariantTranches 실행
    sp.call(f'sh germline_short/filter_variant_tranches.sh {scored_hard_vcf_path_indel} {cnn_filtered_path_indel} {INTERVAL_FILE_PATH} {CNN_model} {seq_type}', shell=True)




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



if gs_work_type == 'ft':
    loop_count = 0

    while True:
        try:
            mapping_time = time.time()
            err_msg = f'An_error_occurred_in_consolidating_gvcfs.sh:_Consolidating_GVCF_files_was_failed.'
            # sp.check_call(fr'sh germline_short/funcotator.sh {}', shell=True)
            break

        except sp.CalledProcessError as e:
            sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
            loop_count += 1
            if loop_count > max_looping:
                exit(0)