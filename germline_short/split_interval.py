
# split_interval.py로 interval file 나누고 진행

import pandas as pd
import os
import numpy as np

from pandas.io.parquet import FastParquetImpl


input_dir = r'/data_244/refGenome/hg38/v0/interval_file/split_interval'
interval_name = r'S07604514_Padded.bed'

prefix = r'hg38_S07604514_Padded_'
suffix = r'.bed'


interval_path = os.path.join(input_dir, interval_name)

intv_df = pd.read_csv(interval_path, \
    low_memory=False, sep='\t', names=['Chr', 'Start', 'End', 'info'])

intv_df.drop(['info'], axis=1, inplace=True)

# print(intv_df)
chr_component_lst = intv_df['Chr'].unique().tolist()
# print(chr_component_lst)
# print(type(chr_component_lst))

splited_df_obj = intv_df.groupby('Chr')
# print(splited_df_obj)

# print(splited_df_obj.get_group('chr1'))


for i in range(len(chr_component_lst)):
    splited_df = splited_df_obj.get_group(chr_component_lst[i])
    f_name = chr_component_lst[i]
    print(splited_df)
    print(f_name)
    
    out_f_name = prefix + f_name + suffix
    out_path = os.path.join(input_dir, out_f_name)
    
    # print(out_path)
    splited_df.to_csv(out_path, sep='\t', header=False, index=False)
    
    
    
    
