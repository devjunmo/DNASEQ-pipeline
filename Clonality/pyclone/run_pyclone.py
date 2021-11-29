
from glob import glob
import subprocess as sp
import os
import pandas as pd


# input_tsv_dir = r'E:/UTUC_data/WES/rmhd_maf/mutect/mutect2/pyclone_inputs/sample2'
# input_tsv_dir = r'E:/UTUC_data/WES/rmhd_maf/mutect/mutect2/pyclone_inputs/sample1'
input_tsv_dir = r'E:/UTUC_data/gdc_hg38/maf/1st_lynch/DP_AF_filtered_maf/pyclone_inputs'
# input_tsv_dir = r'E:/UTUC_data/gdc_hg38/maf/3rd/DP_AF_filtered_maf/True_maf/True_positive_maf/pyclone_inputs'

input_format = r'*.tsv'

tumor_contents_info = r'E:/UTUC_data/gdc_hg38/UTUC_pyclone_tumor_contents.csv' # file_name    tumor_contents  CSV file

is_qsub = True

pbs_N = "utuc1_pyclone"
pbs_o = os.path.join(input_tsv_dir, pbs_N)
pbs_j = "oe"
pbs_l_core = 2
SRC_DIR = r"/data_244/src/ips_germ_210805/DNASEQ-pipeline/Clonality/pyclone/"


tc_df = pd.read_csv(tumor_contents_info)
tc_df.set_index('file_name', inplace=True)

tc_dict = tc_df.to_dict('index') # {'20S-14292-A1-7.tsv': {'tumor_contents': 0.77}, ... } dict 형태. fname

print(tc_dict)


input_path_lst = glob(os.path.join(input_tsv_dir, input_format))

print(input_path_lst)


# print(tc_dict['20S-14292-A1-7.tsv']['tumor_contents'])

# exit(0)



for i in range(len(input_path_lst)):

    f_dir, f_name = os.path.split(input_path_lst[i])

    output_dir = os.path.join(f_dir, 'Output_' + f_name.split(r'.')[0])

    sample_tc = tc_dict[f_name]['tumor_contents']

    if os.path.isdir(output_dir) is False:
        os.mkdir(output_dir)

    if is_qsub is True:
        sp.call(f'echo "sh {SRC_DIR}run_pyclone_qsub.sh {input_path_lst[i]} {output_dir} {sample_tc}" | qsub \
                                                -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
    else:
        sp.call('PyClone run_analysis_pipeline --in_files {0} --working_dir {1} \
            --tumour_contents {2}'.format(input_path_lst[i], output_dir, tc_dict[f_name]['tumor_contents']), shell=True)
        

# "PyClone run_analysis_pipeline --in_files {0} --working_dir {1} \
#             --tumour_contents {2}"".format(input_path_lst[i], output_dir, tumor_contents[i])"

    # break
