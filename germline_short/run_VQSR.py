
# Gathering된 VCF에 대해 SNP/INDEL 모드로 각각 VQSR 과정 진행

import os
from glob import glob
import pandas as pd
import subprocess as sp


input_dir = r''
output_dir = r''
output_prefix = r''
interval_path = r''
ref_genome_ver = r'hg38'

seq_type = r'WES'
var_type = r'SNP'



# SNP - make recal table
sp.call(f'nohup ')


# SNP - apply VQSR
sp.call()
