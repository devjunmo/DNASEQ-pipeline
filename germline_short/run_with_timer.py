import subprocess as sp
import glob
import natsort
import time
from time import sleep

#######################################
run_concurr = 4 # 동시에 4개 돌림
sleep_time = 6000 # 100분, 완전 넉넉잡은값(평균80임)

INPUT_DIR = r'/home/jun9485/data/WES/HN00144124/'
TARGET_FILE = '*.bam'

seq_type = 'WES'

#######################################
ref = r'/home/jun9485/data/refGenome/b37/human_g1k_v37.fasta'
out_prefix = r'/home/jun9485/data/WES/HN00144124/gs/single/'
interval = r'/home/jun9485/data/refGenome/b37/SureSelect_v6_processed.bed'
mode = 'single' 
#######################################


 
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
    count = count + 1

    if count == run_concurr:
        count = 0
        sleep(sleep_time)
