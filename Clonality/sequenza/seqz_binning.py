
import pandas as pd
import subprocess as sp
import os
from glob import glob



input_dir = r'/data_244/utuc/sequenza/seqz/'

input_format = r'*.seqz.gz'

output_dir_name = r'small/'

output_suffix = r'.seqz.gz'

tool_path = r'/home/pbsuser/miniconda3/envs/sequenza/bin/sequenza-utils'

output_dir = input_dir + output_dir_name

if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)

############### pbs config ################

pbs_N = "seqz.mutect2"
pbs_o = output_dir + r"pbs_out/"
pbs_j = "oe"
pbs_l_core = 3
SRC_DIR = r"/data_244/src/utuc_sequenza/DNASEQ-pipeline/sequenza/"

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)

###########################################

input_lst = glob(input_dir + input_format)


for i in range(len(input_lst)):
    input_seqz = input_lst[i]
    s_name = input_seqz.split(r'/')[-1].split('.')[0]
    # print(t_name)

    # break
    
    # # [Tumor bam path] [Normal bam path] [Normal name] [Germline src] [Ref genome] [interval] [Output fname] [PON]


    output_path = output_dir + s_name + output_suffix

    sp.call(rf'echo "{tool_path} seqz_binning --seqz {input_seqz} -w 50 -o {output_path}" \
        | qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)


exit(0)
