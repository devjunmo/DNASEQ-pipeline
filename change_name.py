import subprocess as sp
from glob import glob
import os



input_dir = '/data/utuc/RNAseq/processing_Data'

input_lst = glob(os.path.join(input_dir, '*.gz'))

for f in input_lst:

    file_name_comp = f.split(r'/')[-1].split('.')[0].split('_')
    print(file_name_comp)

    new_f_name = file_name_comp[0] + '-' + file_name_comp[1] + '_' + file_name_comp[2] + '.fastq.gz'

    new_path = os.path.join(input_dir, new_f_name)

    sp.call(rf'mv {f} {new_path}', shell=True)

