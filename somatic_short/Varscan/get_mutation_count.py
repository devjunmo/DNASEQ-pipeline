import os
import pandas as pd
from glob import glob

root_dir = r'E:/stemcell/somatic_analysis/varscan'
file_format = r'*.snp'

file_lst = glob(os.path.join(root_dir, file_format))

res_df = pd.DataFrame(columns=['Germline', 'LOH', 'Somatic', 'Unknown'])

for f in file_lst:

    vcf_df = pd.read_csv(f, sep='\t')
    print(f)
    sample_name = f.split('\\')[-1].split(r'.')[0] # 유동적
    print(sample_name)
    
    germline_count = vcf_df[vcf_df['somatic_status']=='Germline'].shape[0]
    loh_count = vcf_df[vcf_df['somatic_status']=='LOH'].shape[0]
    somatic_count = vcf_df[vcf_df['somatic_status']=='Somatic'].shape[0]
    unknown_count = vcf_df[vcf_df['somatic_status']=='Unknown'].shape[0]
    
    
    res_df.loc[sample_name] = [germline_count, loh_count, somatic_count, unknown_count]


print(res_df)

output_dir = os.path.join(root_dir, 'varscan_muation_count.csv')

res_df.to_csv(output_dir)