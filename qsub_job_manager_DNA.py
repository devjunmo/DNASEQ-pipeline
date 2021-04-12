import subprocess as sp
import glob
import natsort
import time
from time import sleep

# script형태의 python 파일
# 사용시 hyper parameters에 해당하는 부분 유동적으로 수정
# paired end 기준으로 돌아감 

####################### hyper parameters ########################################
sample_group_name = 'HN00144124'
is_making_input_list = True

REF_GENOME_PATH = '/home/jun9485/data/refGenome/b37/human_g1k_v37.fasta' 
INTERVAL_FILE_PATH = '/home/jun9485/data/refGenome/b37/SureSelect_v6_processed.bed'
seq_type = "WES"

# Fastqc(qc) / preprocessing(pp) / germShort(gs) / somaticShort(ss) / germCNV(gc) / somaticCNV(sc)
WORKING_TYPE = "pp"

# QC
qc_output_path = 'pass'

# Data pre-processing for variant discovery           
INPUT_DIR = r'/home/jun9485/data/WES/HN00144124/'   # 이 디렉토리에 계속 생성시킬것
RAW_READS = r'*.fastq.gz'                                                         

# Germline short variant discovery (SNPs + Indels)
PROCESSED_BAM = r'*.bam'
GSDIR = r'gs/'


# Somatic short variant discovery (SNVs + Indels)

# Germline copy number variant discovery (CNVs)

# Somatic copy number variant discovery (CNVs)

#################################################################################

def mk_init_file_list(_input_dir, _raw_read_form, group_name): # fastq파일의 부재로 중간지점 스타트 불가능한 문제 해결목적
    _input_path_list = glob.glob(_input_dir + _raw_read_form)
    _input_path_list = natsort.natsorted(_input_path_list)
    _output_path = _input_dir + sample_group_name + '.txt'
    
    f = open(f'{_output_path}', mode='w')
    for i in range(len(_input_path_list)):
        data = f'{_input_path_list[i]}\n'
        f.write(data)
    f.close


if WORKING_TYPE == 'qc':
    pass


if WORKING_TYPE == "pp":
    # Data pre-processing for variant discovery
    if is_making_input_list is True:
        mk_init_file_list(INPUT_DIR, RAW_READS, sample_group_name)
    # 한줄씩 읽어서 input_path_list에 넣기 
    f = open(rf'{INPUT_DIR}{sample_group_name}.txt', 'r')
    input_path_list = []
    for i in f.readlines():
        input_path_list.append(i[:-1])
    # input_path_list = glob.glob(INPUT_DIR + RAW_READS)    
    input_path_list = natsort.natsorted(input_path_list)
    path_len = len(input_path_list)

    print('입력할 paired end reads의 총 수 =', path_len, '\n')
    print(input_path_list)

    # exit(0) # path list 확인하고 싶으면 이거 풀기

    for i in range(path_len):
        if i%2 == 0: # 짝수면
            print(f'{input_path_list[i]} and {input_path_list[i+1]} preprocessing...')
            process = round(i/path_len, 2) * 100
            print(f'{process}% 진행')

            read1 = input_path_list[i]
            read2 = input_path_list[i+1]
            read_name = input_path_list[i].split('.')[-3].split(r'/')[-1].split(r'_')[-2] # Teratoma-13
            prefix = INPUT_DIR + read_name

            # "ha:b:n:p:i:", ["help", "readA=", "readB=", "readName=", "prefix=", "inputDir="]
            sp.call(f'nohup python preprocessing/preprocessing_DNA.py -a {read1} -b {read2} -n {read_name} -p {prefix} -i {INPUT_DIR} \
                -R {REF_GENOME_PATH} -L {INTERVAL_FILE_PATH} -y {seq_type} &', shell=True)
            sleep(6000) # 100분 sleep


elif WORKING_TYPE == "gs":
    # Germline short variant discovery (SNPs + Indels) 
    input_path_list = glob.glob(INPUT_DIR + PROCESSED_BAM)    
    input_path_list = natsort.natsorted(input_path_list)
    path_len = len(input_path_list)

    print('입력할 sample의 총 수 =', path_len, '\n')
    print(input_path_list)

    # exit(0) # path list 확인하고 싶으면 이거 풀기

    # read_name_list = []
    # prefix_list = []
    # gvcf_list = []

    INPUT_GS_DIR = INPUT_DIR + GSDIR

    for i in range(path_len):
        process = round(i/path_len, 2) * 100
        print(f'{process}% 진행')

        bamfile = input_path_list[i]
        # sample: recal_deduped_sorted_hiPS36-C.bam
        read_name = input_path_list[i].split('.')[-2].split(r'/')[-1].split(r'_')[-1] # hiPS36-C
        
        prefix = INPUT_GS_DIR + read_name
        
        output_gvcf = INPUT_GS_DIR + read_name + '.g.vcf.gz'

        # HaplotypeCaller 실행
        sp.call(f'qsub ~/src/qsub.1 sh germline_short/make_GVCF.sh {REF_GENOME_PATH} {output_gvcf} {bamfile} {INTERVAL_FILE_PATH} {seq_type}', shell=True)


    while True:
        sleep(300)
        val = sp.check_output(f'qstat', shell=True, universal_newlines=True)
        if val == "":
            print("GVCF 생성 완료")
            break
    

    sp.call(f'python germline_short/variant_calling_gs.py -g {INPUT_GS_DIR} -R {REF_GENOME_PATH} -L {INTERVAL_FILE_PATH} -y {seq_type}', shell=True)
        
    

elif WORKING_TYPE == "ss":
    pass
elif WORKING_TYPE == "gc":
    pass
elif WORKING_TYPE == "sc":
    pass


        
# case 2. germline short
