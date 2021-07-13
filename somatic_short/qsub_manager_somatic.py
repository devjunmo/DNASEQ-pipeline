import os
from glob import glob
import subprocess as sp
import pandas as pd


############## hyper params ##############

seq_type = 'WES'

input_dir = r'/data_244/utuc/'
input_format = r'recal_*.bam'

output_dir = input_dir + r'somatic_call/'

ref_dir = r'/data_244/refGenome/b37/'

ref_genome_path = ref_dir + 'human_g1k_v37.fasta'

PON_path = ref_dir + r'somatic_src/mutect_PON_20151116_1000samples_over10.splited.vcf'
germ_src_path = ref_dir + r'somatic_src/af-only-gnomad.raw.sites.vcf.gz'
sec_src_path = ref_dir + r'somatic_src/small_exac_common_3.vcf.gz'

interval_path = ref_dir + r'SureSelect_v6_processed.bed'

pair_info = r'/data_244/utuc/utuc_NT_pair.csv'


if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


############### pbs config ################

pbs_N = "utuc.DNA.somatic"
pbs_o = output_dir + r"pbs_out/"
pbs_j = "oe"
pbs_l_core = 3
SRC_DIR = r"/data_244/src/utuc_pp/DNASEQ-pipeline/somatic_short/"

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)

###########################################




os.chdir(SRC_DIR)


pair_df = pd.read_csv(pair_info)
pair_df.set_index('Tumor', inplace=True)

pair_dict = pair_df.to_dict('index') # {tumor : {normal:_ grade:_} dict 형태. fname

print(pair_dict)

input_lst = glob(input_dir + input_format)

# print(input_lst)

for i in range(len(input_lst)):
    input_bam = input_lst[i]
    t_name = input_bam.split(r'/')[-1].split('.')[0].split(r'_')[-1] # tumor
    print(t_name)
    
    # # [Tumor bam path] [Normal bam path] [Normal name] [Germline src] [Ref genome] [interval] [Output fname] [PON]

    try:
        target_normal_name = pair_dict[t_name]['Normal']
        # pair_dict[f_name]['Tumor_Grade']
        sp.call(f'echo "python {SRC_DIR}run_mutect2.py -n {target_normal_name} -t {t_name} -I {input_dir} -R {ref_genome_path} -L {interval_path} -y {seq_type} \
                                        -P {PON_path} -S {sec_src_path} -G {germ_src_path} -O {output_dir}" | qsub \
                                        -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)

    except KeyError as e:
        print(f'{t_name} does not have target normal sample')
        continue
    






