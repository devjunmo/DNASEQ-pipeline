from ntpath import join
import pandas as pd
import os
from glob import glob
import natsort

from pandas.core.arrays.sparse import dtype


pd.set_option('display.max_seq_items', None) # colname 생략 없이 출력
pd.set_option('display.max_columns', None) # col 생략 없이 출력


maf_input_dir = r'E:/UTUC_data/WES/rmhd_maf/mutect/mutect2/filtered_maf/pyclone/'
maf_input_format = r'*.maf'

seqz_input_dir = r'E:/UTUC_data/WES/sequenza/res/'
seqz_input_format = r'*_segments.txt'

output_dir_name = r'pyclone_inputs/'
output_dir = maf_input_dir + output_dir_name

NORMAL_CN = 2


# result_df = pd.DataFrame(columns=['mutation_id', 'ref_counts', 'var_counts', \
#                                     'normal_cn', 'minor_cn', 'major_cn'])


need_maf_col = ['Chromosome', 'Start_Position', 'End_Position', 'Reference_Allele', \
                'Tumor_Seq_Allele2', 'Tumor_Sample_Barcode', 't_ref_count', 't_alt_count']

need_seqz_col = ['chromosome', 'start.pos', 'end.pos', 'A', 'B']


if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


maf_input_lst = glob(maf_input_dir + maf_input_format)
seqz_input_lst = glob(seqz_input_dir + seqz_input_format)

maf_input_lst = natsort.natsorted(maf_input_lst)
seqz_input_lst = natsort.natsorted(seqz_input_lst)


print(maf_input_lst)
print(seqz_input_lst)


tst_maf = pd.read_csv(maf_input_lst[0], sep='\t')

# print(tst_maf.columns)
# print(tst_maf['Tumor_Sample_Barcode'])
# print(tst_maf['Reference_Allele'])
# print(tst_maf['Tumor_Seq_Allele1'])
# print(tst_maf['Tumor_Seq_Allele2'])


# exit(0)

def in_range(n, start, end):
    return start <= n <= end if end >= start else end <= n <= start


for i in range(len(maf_input_lst)):

    result_df = pd.DataFrame(columns=['mutation_id', 'ref_counts', 'var_counts', \
                                    'normal_cn', 'minor_cn', 'major_cn'])
    print(result_df)


    # sample_name = maf_input_lst[i].split('\\')[-1].split(r'_')[0] # 20S-14292-A1-7     /home/jun/data/       ej-001Sample.maf
    sample_name = maf_input_lst[i].split('\\')[-1].split(r'.')[0].split(r'_')[-1]
    print(sample_name)

    maf_df = pd.read_csv(maf_input_lst[i], sep='\t')
    # print(maf_df.columns)

    maf_df = maf_df[need_maf_col]
    # print(maf_df)
    # print(maf_df.dtypes)

    seqz_df = pd.read_csv(seqz_input_lst[i], sep='\t')
    seqz_df = seqz_df[need_seqz_col]
    # print(seqz_df)
    # print(seqz_df.dtypes)

    
    for m_index, m_rows in maf_df.iterrows():
        # print(m_rows)

        for s_index, s_rows in seqz_df.iterrows():
            # print(s_rows)

            if m_rows['Chromosome'] == s_rows['chromosome']:
                if in_range(m_rows['Start_Position'], s_rows['start.pos'], s_rows['end.pos']) and \
                    in_range(m_rows['End_Position'], s_rows['start.pos'], s_rows['end.pos']): # 사이값에 존재 한다면
                    input_row = ['_'.join([m_rows['Chromosome'], str(m_rows['Start_Position']), str(m_rows['End_Position']), \
                        m_rows['Reference_Allele'], m_rows['Tumor_Seq_Allele2']]), \
                        m_rows['t_ref_count'], m_rows['t_alt_count'], NORMAL_CN, s_rows['B'], s_rows['A']]
                    
                    result_df = result_df.append(pd.Series(input_row, index=result_df.columns), ignore_index=True)

                    break # 세번째 루프를 끝내고 그 다음 maf 포지션으로 가겠다는것 

    
    output_path = output_dir + sample_name + '.tsv'
    result_df.to_csv(output_path, sep='\t', index=False)


    