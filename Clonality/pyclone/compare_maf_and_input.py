
"""
디버깅 용도, maf로 부터 tsv가 제대로 나왔는지 shape 정보로 확인
"""

import pandas as pd
from glob import glob
import os
import natsort


pd.set_option('display.max_seq_items', None) # colname 생략 없이 출력
pd.set_option('display.max_columns', None) # col 생략 없이 출력


# maf_input_dir = r'E:/UTUC_data/gdc_hg38/maf/3rd/DP_AF_filtered_maf/True_maf/True_positive_maf'
# maf_input_dir = r'E:/UTUC_data/gdc_hg38/maf/5th/DP_AF_filtered_maf/exclude_filterTag_utuc/True_maf/True_positive_maf'
maf_input_dir = r'E:/UTUC_data/gdc_hg38/maf/1st_lynch/DP_AF_filtered_maf'
maf_input_format = r'*.maf'

pyclone_input_dir = os.path.join(maf_input_dir, 'pyclone_inputs')
pyclone_input_format = r'*.tsv'





# output_dir_name = r'pyclone_inputs_val/'
# output_dir = pyclone_input_dir + output_dir_name


# if os.path.isdir(output_dir) is False:
#     os.mkdir(output_dir)


maf_input_lst = natsort.natsorted(glob(os.path.join(maf_input_dir, maf_input_format)))
pyclone_input_lst = natsort.natsorted(glob(os.path.join(pyclone_input_dir, pyclone_input_format)))

print(maf_input_lst)
print(pyclone_input_lst)


for i in range(len(maf_input_lst)):
    # sample_name = maf_input_lst[i].split('\\')[-1].split(r'_')[0] # 20S-14292-A1-7
    sample_name = os.path.splitext(pyclone_input_lst[i])[0].split('\\')[-1]
    print(sample_name)

    print('maf count-----')

    maf_df = pd.read_csv(maf_input_lst[i], sep='\t')
    print(maf_df.shape[0])


    print('pyclone input count-----')

    pyc_df = pd.read_csv(pyclone_input_lst[i], sep='\t')
    print(pyc_df.shape[0])


    print('--------')

    print('diff:', ((maf_df.shape[0] - pyc_df.shape[0])/maf_df.shape[0])*100, '%')


    print('\n-------------')