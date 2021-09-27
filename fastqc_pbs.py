import subprocess as sp
import glob
import natsort
import time
from time import sleep
import os


# qsub 사용하지 않고 순차적으로 돌리는 코드

INPUT_DIR = r'/data_244/stemcell/RNA/RNA4/'
OUTPUT_DIR_NAME = r'fastqc/'


RAW_READS = r'*.fastq.gz'  

file_type = 'fastq'

OUTPUT_DIR = INPUT_DIR + OUTPUT_DIR_NAME

fastqc_path = r'/home/pbsuser/FastQC/fastqc'

if os.path.isdir(OUTPUT_DIR) is False:
    os.mkdir(OUTPUT_DIR)


############### pbs config ################

pbs_N = "stem.RNA.qc"
pbs_o = OUTPUT_DIR + r"pbs_out/"
pbs_j = "oe"
pbs_l_core = 1


if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)

###########################################


input_path_list = glob.glob(INPUT_DIR + RAW_READS)    
input_path_list = natsort.natsorted(input_path_list)
path_len = len(input_path_list)

print('QC할 paired end reads의 총 수 =', path_len, '\n')
print(input_path_list)

# exit(0)

for i in range(path_len):

    read = input_path_list[i]

    # fastqc -o ~/data/WGS/fastqc/ -f fastq -t 4 Teratoma-17_R1.fastq.gz
    # sp.call(f'fastqc -o {OUTPUT_DIR} -f {file_type} {read}', shell=True)

    sp.call(f'echo "{fastqc_path} -o {OUTPUT_DIR} -f {file_type} {read}" | qsub \
                        -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)

