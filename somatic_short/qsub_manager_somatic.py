import os
from glob import glob
import subprocess as sp
import pandas as pd


############## hyper params ##############

seq_type = 'WES'

input_dir = r'/data_244/utuc/'
input_format = r'recal_*.bam'

# output_dir = input_dir + r'somatic_call/'
output_dir = input_dir + r'somatic_call_SID/'

ref_dir = r'/data_244/refGenome/b37/'

ref_genome_path = ref_dir + 'human_g1k_v37.fasta'

PON_path = ref_dir + r'somatic_src/mutect_PON_20151116_1000samples_over10.splited.vcf'
germ_src_path = ref_dir + r'somatic_src/af-only-gnomad.raw.sites.vcf.gz'
sec_src_path = ref_dir + r'somatic_src/small_exac_common_3.vcf.gz'

interval_path = ref_dir + r'SureSelect_v6_processed.bed'

pair_info = r'/data_244/utuc/utuc_NT_pair.csv'

run_type = 'SID' # MT1 (Mutect1), MT2(Mutect2), SID (somatic indel detector)


java7_path = r'/usr/lib/jvm/java-1.7.0/bin/java'
mutect1_path = r'/home/pbsuser/mutect1/mutect-1.1.7.jar'
gatk_legacy_path = r'/home/pbsuser/LagacyGATK/GenomeAnalysisTK.jar'

dbsnp_path = ref_dir + r'dbsnp_138.b37.vcf'
cosmic_path = ref_dir + r'cosmic_v54_120711.b37.vcf'


if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


############### pbs config ################

pbs_N = "utuc.mutect2.2"
pbs_o = output_dir + r"pbs_out/"
pbs_j = "oe"
pbs_l_core = 2
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
        normal_bam = input_dir + 'recal_deduped_sorted_' + target_normal_name + '.bam'
        # pair_dict[f_name]['Tumor_Grade']

        if run_type == 'MT2':
            sp.call(f'echo "python {SRC_DIR}run_mutect2.py -n {target_normal_name} -t {t_name} -I {input_dir} -R {ref_genome_path} -L {interval_path} -y {seq_type} \
                                            -P {PON_path} -S {sec_src_path} -G {germ_src_path} -O {output_dir}" | qsub \
                                            -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
        elif run_type == 'MT1':
            out_txt_path = output_dir + t_name + '.mutect1.txt'
            out_vcf_path = output_dir + t_name + '.mutect1.vcf'
            sp.call(f'echo "sh {SRC_DIR}mutect1.sh {input_bam} {normal_bam} {ref_genome_path} {interval_path} {PON_path} \
                                                    {out_txt_path} {out_vcf_path} {dbsnp_path} {cosmic_path} {seq_type} {java7_path} {mutect1_path}" | qsub \
                                                    -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)

        elif run_type == 'SID':
            out_vcf_path = output_dir + t_name + '.somaticindelocator.vcf'
            sp.call(f'echo "sh {SRC_DIR}somaticIndelDetector.sh {input_bam} {normal_bam} {ref_genome_path} {interval_path} {PON_path} \
                                                    {out_vcf_path} {dbsnp_path} {cosmic_path} {seq_type} {java7_path} {gatk_legacy_path}" | qsub \
                                                    -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)

    except KeyError as e:
        print(f'{t_name} does not have target normal sample')
        continue
    






