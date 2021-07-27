
import pandas as pd
import subprocess as sp
import os
from glob import glob


root_dir = r'/data_244/utuc/'
sequenza_dir = r'sequenza/'

input_dir = root_dir + sequenza_dir

ref_path = r'/data_244/refGenome/b37/human_g1k_v37.fasta'

bam_format = r'recal_*.bam'

wig_file_path = input_dir + r'b37.gc50Base.wig.gz'

output_dir_name = r'seqz/'

output_suffix = r'.seqz.gz'

pair_info = r'/data_244/utuc/utuc_NT_pair.csv'

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

pair_df = pd.read_csv(pair_info)
pair_df.set_index('Tumor', inplace=True)

pair_dict = pair_df.to_dict('index') # {tumor : {normal:_ grade:_} dict 형태. fname

print(pair_dict)

input_bam_lst = glob(root_dir + bam_format)


for i in range(len(input_bam_lst)):
    input_tumor_bam = input_bam_lst[i]
    t_name = input_tumor_bam.split(r'/')[-1].split('.')[0].split(r'_')[-1] # 20S-14292-A1-7
    # print(t_name)

    # break
    
    # # [Tumor bam path] [Normal bam path] [Normal name] [Germline src] [Ref genome] [interval] [Output fname] [PON]

    try:
        target_normal_name = pair_dict[t_name]['Normal']
        normal_bam = root_dir + 'recal_deduped_sorted_' + target_normal_name + '.bam'
        # pair_dict[f_name]['Tumor_Grade']

        output_path = output_dir + t_name + output_suffix

        # sp.call('sequenza−utils bam2seqz -n {normal_bam} -t {input_tumor_bam} --fasta {ref_path} \
        # -gc {wig_file_path} -o {output_path}')

        sp.call(rf'echo "{tool_path} bam2seqz -n {normal_bam} -t {input_tumor_bam} --fasta {ref_path} -gc {wig_file_path} -o {output_path}" \
            | qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)

    except KeyError as e:
        print(f'{t_name} does not have target normal sample')
        continue
    

exit(0)
