import subprocess as sp
import glob
import natsort
import time
from time import sleep

#######################################

work_type = 'FilterVariantTranches'

run_concurr = 3 # 동시에 1개 돌림
sleep_time = 80 # 넉넉잡은 시간

INPUT_DIR = r'/home/jun9485/data/WES/HN00144124/'
TARGET_FILE = '*.bam'

seq_type = 'WES'

###########[ HaplotypeCaller ]###########
ref = r'/home/jun9485/data/refGenome/b37/human_g1k_v37.fasta'
out_prefix = r'/home/jun9485/data/WES/HN00144124/gs/single/'
interval = r'/home/jun9485/data/refGenome/b37/SureSelect_v6_processed.bed'
mode = 'single' 
#######################################


###########[ CNNScoreVariants ]###########
docker_INPUT_BAM_DIR = r'/data_244/WES/HN00144124/processed/'
bam_file = '*.bam'
docker_INTERVAL = r'/data_244/refgenome/b37/SureSelect_v6_processed.bed'
docker_REFGENOME = r'/data_244/refgenome/b37/human_g1k_v37.fasta'
docker_INPUT_VCF_DIR = r'/data_244/WES/HN00144124/processed/gs/single/'
input_vcf_file = '*.vcf.gz'

model = "2D"
seq_type = "WES"

##########################################

########[ FilterVariantTranches ]#########
input_scored_vcf_file = 'scored_*.vcf'

##########################################


if work_type == 'HaplotypeCaller':
    input_path_list = glob.glob(INPUT_DIR + TARGET_FILE)    
    input_path_list = natsort.natsorted(input_path_list)
    path_len = len(input_path_list)

    print('입력할 file의 총 수 =', path_len, '\n')
    print(input_path_list)

    exit(0) # path list 확인하고 싶으면 이거 풀기

    count = 0

    for i in range(path_len):
        process = round(i/path_len, 2) * 100
        print(f'{process}% 진행')

        bamfile = input_path_list[i]
        # sample: recal_deduped_sorted_hiPS36-C.bam
        read_name = input_path_list[i].split('.')[-2].split(r'/')[-1].split(r'_')[-1] # hiPS36-C

        prefix = out_prefix + read_name
        
        output_vcf = prefix + '.vcf.gz'
        
        # HaplotypeCaller 실행
        sp.call(f'nohup sh haplotypeCaller.sh {ref} {output_vcf} {bamfile} {interval} {seq_type} {mode} &', shell=True)

        if count == run_concurr:
            count = 0
            sleep(sleep_time)

        

elif work_type == 'CNNScoreVariants':
    input_bam_list = glob.glob(docker_INPUT_BAM_DIR + bam_file)
    input_bam_list = natsort.natsorted(input_bam_list)
    bam_len = len(input_bam_list)

    input_vcf_list = glob.glob(docker_INPUT_VCF_DIR + input_vcf_file) 
    input_vcf_list = natsort.natsorted(input_vcf_list)
    vcf_len = len(input_vcf_list)

    print('input bam file_num =', bam_len, '\n')
    print(input_bam_list)
    
    print('input vcf.gz file_num =', vcf_len, '\n')
    print(input_vcf_list)

    # exit(0)

    count = 0

    if bam_len != vcf_len:
        print('bam file과 vcf.gz file의 갯수가 1대1로 매칭되지 않음. 확인후 다시시도.')
        exit(1)

    for i in range(bam_len):
        read_name = input_bam_list[i].split('.')[-2].split(r'/')[-1].split(r'_')[-1] # hiPS36-C
        output_vcf_prefix = docker_INPUT_VCF_DIR + 'scored_'
        output_vcf_suffix = '.vcf'
        output_vcf = output_vcf_prefix + read_name + output_vcf_suffix
    
        # CNNScoreVariants 실행
        sp.call(f'nohup sh cnn_score_variants.sh {input_bam_list[i]} {input_vcf_list[i]} {docker_REFGENOME} {output_vcf} {docker_INTERVAL} {model} {seq_type} &', shell=True)

        count = count + 1

        if count == run_concurr:
            count = 0
            sleep(sleep_time)


# FilterVariantTranches
elif work_type == 'FilterVariantTranches':

    input_vcf_list = glob.glob(docker_INPUT_VCF_DIR + input_scored_vcf_file) 
    input_vcf_list = natsort.natsorted(input_vcf_list)
    vcf_len = len(input_vcf_list)
    
    print('input vcf.gz file_num =', vcf_len, '\n')
    print(input_vcf_list)

    # exit(0)

    count = 0

    for i in range(vcf_len):
        read_name = input_vcf_list[i].split('.')[-2].split(r'/')[-1].split(r'_')[-1] # hiPS36-C
        output_vcf_prefix = docker_INPUT_VCF_DIR + 'filtered_scored_'
        output_vcf_suffix = '.vcf'
        output_vcf = output_vcf_prefix + read_name + output_vcf_suffix
    
        # FilterVariantTranches 실행
        sp.call(f'nohup sh filter_variant_tranches.sh {input_vcf_list[i]} {output_vcf} {docker_INTERVAL} {model} {seq_type} &', shell=True)

        count = count + 1

        if count == run_concurr:
            count = 0
            sleep(sleep_time)
