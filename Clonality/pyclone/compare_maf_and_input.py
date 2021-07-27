import pandas as pd
from glob import glob
import os
import natsort


pd.set_option('display.max_seq_items', None) # colname 생략 없이 출력
pd.set_option('display.max_columns', None) # col 생략 없이 출력


maf_input_dir = r'E:/UTUC_data/WES/rmhd_maf/mutect/mutect2/'
maf_input_format = r'*.maf'

pyclone_input_dir = r'E:/UTUC_data/WES/rmhd_maf/mutect/mutect2/pyclone_inputs/'
pyclone_input_format = r'*.tsv'

output_dir_name = r'pyclone_inputs_val/'
output_dir = pyclone_input_dir + output_dir_name


if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


maf_input_lst = glob(maf_input_dir + maf_input_format)
pyclone_input_lst = glob(pyclone_input_dir + pyclone_input_format)

maf_input_lst = natsort.natsorted(maf_input_lst)
pyclone_input_lst = natsort.natsorted(pyclone_input_lst)

print(maf_input_lst)
print(pyclone_input_lst)


for i in range(len(maf_input_lst)):
    sample_name = maf_input_lst[i].split('\\')[-1].split(r'_')[0] # 20S-14292-A1-7
    print(sample_name)

    print('\nmaf-----')

    maf_df = pd.read_csv(maf_input_lst[i], sep='\t')
    print(maf_df.shape[0])


    print('pyc-----')

    pyc_df = pd.read_csv(pyclone_input_lst[i], sep='\t')
    print(pyc_df.shape[0])


    print('----- % -----')

    print(((maf_df.shape[0] - pyc_df.shape[0])/maf_df.shape[0])*100, '%')


    print('\n-------------')