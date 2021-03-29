import subprocess as sp
import glob
import natsort
import time

# script형태의 python 파일
# 사용시 hyper parameters에 해당하는 부분 유동적으로 수정
# paired end 기준으로 돌아감 

# 추가할 내용
# python qsub_manager.py --job "preprocessing(pp) / germShort(gs) / somaticShort(ss) / germCNV(gc) / somaticCNV(sc) " 
# 

####################### hyper parameters ########################################     

# Data pre-processing for variant discovery           
                                      
INPUT_DIR = r'/home/jun9485/data/WES/HN00144124/retry/'   # 이 디렉토리에 계속 생성시킬것
RAW_READS = r'*.fastq.gz'                                                         

# Germline short variant discovery (SNPs + Indels)

# Somatic short variant discovery (SNVs + Indels)

# Germline copy number variant discovery (CNVs)

# Somatic copy number variant discovery (CNVs)

#################################################################################


# case 1. data pre-processing

input_path_list = glob.glob(INPUT_DIR + RAW_READS)    
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
        sp.call(f'qsub ~/src/qsub.1 python preprocessing/preprocessing_DNA.py -a {read1} -b {read2} -n {read_name} -p {prefix} -i {INPUT_DIR}', shell=True)
        

# case 2. germline short