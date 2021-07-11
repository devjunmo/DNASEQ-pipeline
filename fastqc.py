import subprocess as sp
import glob
import natsort
import time
from time import sleep
import os


# qsub 사용하지 않고 순차적으로 돌리는 코드

INPUT_DIR = r'/home/jun9485/data/utuc/'
OUTPUT_DIR_NAME = r'fastqc/'


RAW_READS = r'*.fastq.gz'  
thread = 6
file_type = 'fastq'

OUTPUT_DIR = INPUT_DIR + OUTPUT_DIR_NAME

if os.path.isdir(OUTPUT_DIR) is False:
    os.mkdir(OUTPUT_DIR)


input_path_list = glob.glob(INPUT_DIR + RAW_READS)    
input_path_list = natsort.natsorted(input_path_list)
path_len = len(input_path_list)

print('QC할 paired end reads의 총 수 =', path_len, '\n')
print(input_path_list)

# exit(0)

for i in range(path_len):
    print(f'{input_path_list[i]} preprocessing...')
    process = round(i/path_len, 2) * 100
    print(f'{process}% 진행')

    read = input_path_list[i]

    # fastqc -o ~/data/WGS/fastqc/ -f fastq -t 4 Teratoma-17_R1.fastq.gz
    sp.call(f'fastqc -o {OUTPUT_DIR} -f {file_type} -t {thread} {read}', shell=True)

