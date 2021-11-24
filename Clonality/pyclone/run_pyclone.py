
from glob import glob
import subprocess as sp
import os


# input_tsv_dir = r'E:/UTUC_data/WES/rmhd_maf/mutect/mutect2/pyclone_inputs/sample2'
# input_tsv_dir = r'E:/UTUC_data/WES/rmhd_maf/mutect/mutect2/pyclone_inputs/sample1'
input_tsv_dir = r'E:/UTUC_data/gdc_hg38/maf/pyclone_input'

input_format = r'*.tsv'

input_path_lst = glob(os.path.join(input_tsv_dir, input_format))

print(input_path_lst)





for input_tsv in input_path_lst:

    f_dir, f_name = os.path.split(input_tsv)

    output_dir = os.path.join(f_dir, 'Output_' + f_name.split(r'.')[0])

    if os.path.isdir(output_dir) is False:
        os.mkdir(output_dir)

    sp.call('PyClone run_analysis_pipeline --in_files {0} --working_dir {1}'.format(input_tsv, output_dir), shell=True)



    # break
