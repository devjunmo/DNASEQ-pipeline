import os
from glob import glob
import subprocess as sp
import sys
sys.path.append(r'/data/src/DNASEQ-pipeline/jun_tools')
from jun_tools import jun_mtd

print(sys.path)

input_dir = r'/data/stemcell/WES/mouse/ips/bamfiles'
output_dir_name = r'tables'
thread = 5
output_format = 'tsv'

# pbs config

pbs_N = "stem_ips_check"
pbs_o = input_dir + r"pbs_check_mapping_stat/"
pbs_j = "oe"
pbs_l_core = 5
SRC_DIR = r"/data/src/DNASEQ-pipeline/"


output_dir = jun_mtd.set_output_dir(input_dir, output_dir_name)

input_lst = jun_mtd.get_input_path_list(input_dir, '*.bam', True)


def run_check_mapping_stat(_input_lst):
    for i in range(len(_input_lst)):
        _input_bam = _input_lst[i]
        _sample_name = _input_bam.split(r'/')[-1].split(r'.')[0].split(r'_')[0]
        out_name = _sample_name + '_mapping_stat.tsv'
        output_path = os.path.join(output_dir, out_name)
        sp.call(f'echo "samtools flagstats -@ {thread} -O {output_format} {_input_bam} > {output_path}" | qsub \
            -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)


run_check_mapping_stat(input_lst)
