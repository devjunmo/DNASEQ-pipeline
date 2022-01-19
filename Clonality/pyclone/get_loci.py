
# Output dir에 있는 table > loci.tsv를 이름바꿔주고, 한군데다가 복사하는 코드

import os
from glob import glob
import pandas as pd
import shutil


root_dir = r"E:/UTUC_data/gdc_hg38/maf/5th/DP_AF_filtered_maf/exclude_filterTag_utuc/True_positive_maf/pyclone_inputs"

out_dir_lst = glob(os.path.join(root_dir, 'Output_*'))
# print(out_dir_lst)

loci_save_dir = os.path.join(root_dir, 'loci_data')

if os.path.isdir(loci_save_dir) is False:
    os.mkdir(loci_save_dir)


# type: dir or file
def walking_dir(_rootDir, _targetName, _type='dir'): 
    for (root, dirs, files) in os.walk(_rootDir):
        print("# root : " + root)
        if _type=='dir' and len(dirs) > 0:
            for dir_name in dirs:
                if dir_name == _targetName:
                    return os.path.join(_rootDir, dir_name)

        if _type=='file' and len(files) > 0:
            for file_name in files:
                if file_name == _targetName:
                    return os.path.join(_rootDir, file_name)


for out_dir in out_dir_lst:
    table_dir = walking_dir(out_dir, 'tables', _type='dir')
    loci_path = walking_dir(table_dir, 'loci.tsv', _type='file')
    print(loci_path)
    path_prefix, f_name = os.path.split(loci_path)
    print(path_prefix, f_name)
    
    sample_name = pd.read_csv(loci_path, sep='\t').loc[0, 'sample_id']
    print(sample_name)
    loci_rename = sample_name + '_loci.tsv'
    loci_rename_path = os.path.join(path_prefix, loci_rename)
    print(loci_rename)
    
    loci_save_path = os.path.join(loci_save_dir, loci_rename)
    
    shutil.copy(loci_path, loci_rename_path)
    shutil.copy(loci_path, loci_save_path)
    
    
    # break
