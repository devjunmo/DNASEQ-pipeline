from ntpath import join
import pandas as pd
import os
from glob import glob
import natsort

from pandas.core.arrays.sparse import dtype


pd.set_option('display.max_seq_items', None) # colname 생략 없이 출력
pd.set_option('display.max_columns', None) # col 생략 없이 출력


# maf_input_dir = r'E:/UTUC_data/gdc_hg38/maf/5th/DP_AF_filtered_maf/exclude_filterTag_utuc/True_maf/True_positive_maf'
maf_input_dir = r'E:/UTUC_data/gdc_hg38/maf/2nd/DP_AF_filtered_maf/True_maf/True_positive_maf'
maf_input_format = r'*.maf'

# seqz_input_dir = r'E:/UTUC_data/gdc_hg38/CNV/sequenza/utuc_4_5/5th/res'
seqz_input_dir = r'E:/UTUC_data/gdc_hg38/CNV/sequenza/utuc2_3/res/utuc_2nd'
seqz_input_format = r'*_segments.txt'


maf_input_lst = natsort.natsorted(glob(os.path.join(maf_input_dir, maf_input_format)))
seqz_input_lst = natsort.natsorted(glob(os.path.join(seqz_input_dir, seqz_input_format)))

print(maf_input_lst)
print(seqz_input_lst)

# exit(0)

output_dir_name = r'pyclone_inputs'
output_dir = os.path.join(maf_input_dir, output_dir_name)

NORMAL_CN = 2


# result_df = pd.DataFrame(columns=['mutation_id', 'ref_counts', 'var_counts', \
#                                     'normal_cn', 'minor_cn', 'major_cn'])


need_maf_col = ['Chromosome', 'Start_Position', 'End_Position', 'Reference_Allele', \
                'Tumor_Seq_Allele2', 'Tumor_Sample_Barcode', 't_ref_count', 't_alt_count']

need_seqz_col = ['chromosome', 'start.pos', 'end.pos', 'A', 'B']


if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


# print(maf_input_lst)
# print(seqz_input_lst)


# tst_maf = pd.read_csv(maf_input_lst[0], sep='\t')
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
    # print(result_df)


    # sample_name = maf_input_lst[i].split('\\')[-1].split(r'_')[0] # 20S-14292-A1-7     /home/jun/data/       ej-001Sample.maf
    # sample_name = maf_input_lst[i].split('\\')[-1].split(r'.')[0].split(r'_')[-1]
    # print(sample_name)

    maf_df = pd.read_csv(maf_input_lst[i], sep='\t')
    # print(maf_df.columns)
    # print(maf_df)
    sample_name = maf_df.loc[0, 'Tumor_Sample_Barcode']
    # print(sample_name)
    # break

    maf_df = maf_df[need_maf_col]
    # print(maf_df)
    # print(maf_df.dtypes)

    seqz_df = pd.read_csv(seqz_input_lst[i], sep='\t')
    seqz_df = seqz_df[need_seqz_col]
    # print(seqz_df)
    # print(seqz_df.dtypes)

    print(seqz_df)
    print('delete: NaN in seqz table.')
    seqz_df.dropna(inplace=True)
    seqz_df.reset_index(inplace=True, drop=True)
    
    seqz_df = seqz_df.astype({'start.pos':int, 'end.pos':int, 'A':int, 'B':int}, errors='ignore')


    print(seqz_df)
    
    # print(seqz_df.dtypes)

    # exit(0)
    # mutid = chr_start_end_ref_alt
    # for m_index, m_rows in maf_df.iterrows():
    #     # print(m_rows)

    #     for s_index, s_rows in seqz_df.iterrows():
    #         # print(s_rows)

    #         if m_rows['Chromosome'] == s_rows['chromosome']:
    #             if in_range(m_rows['Start_Position'], s_rows['start.pos'], s_rows['end.pos']) and \
    #                 in_range(m_rows['End_Position'], s_rows['start.pos'], s_rows['end.pos']): # 사이값에 존재 한다면
    #                 input_row = ['_'.join([m_rows['Chromosome'], str(m_rows['Start_Position']), str(m_rows['End_Position']), \
    #                     m_rows['Reference_Allele'], m_rows['Tumor_Seq_Allele2']]), \
    #                     m_rows['t_ref_count'], m_rows['t_alt_count'], NORMAL_CN, s_rows['B'], s_rows['A']]
                    
    #                 result_df = result_df.append(pd.Series(input_row, index=result_df.columns), ignore_index=True)

    #                 break # 세번째 루프를 끝내고 그 다음 maf 포지션으로 가겠다는것 

    # mutid = chr:start:end



    # maf_flag = False

    # tmp_m_idx = None
    # tmp_m_rows = None

    # maf_last_idx = maf_df.index[-1]

    for m_index, m_rows in maf_df.iterrows(): # maf loop
        # print(m_rows)
        maf_flag = False
        # tmp_m_idx = m_index
        # tmp_m_rows = m_rows

        # if maf_flag == True:
        #     # print('하나 전 인덱스 저장')
        #     input_row = [':'.join([tmp_m_rows['Chromosome'], str(tmp_m_rows['Start_Position']), str(tmp_m_rows['End_Position'])]), \
        #                 tmp_m_rows['t_ref_count'], tmp_m_rows['t_alt_count'], NORMAL_CN, int(0), int(2)]
        #     result_df = result_df.append(pd.Series(input_row, index=result_df.columns), ignore_index=True)
        
        for s_index, s_rows in seqz_df.iterrows(): # maf row에 대해 segment file 훑기 
            # print(s_rows)
            if m_rows['Chromosome'] == s_rows['chromosome']:
                if in_range(m_rows['Start_Position'], s_rows['start.pos'], s_rows['end.pos']) and \
                    in_range(m_rows['End_Position'], s_rows['start.pos'], s_rows['end.pos']): # 사이값에 존재 한다면

                    input_row = [':'.join([m_rows['Chromosome'], str(m_rows['Start_Position']), str(m_rows['End_Position'])]), \
                        m_rows['t_ref_count'], m_rows['t_alt_count'], NORMAL_CN, s_rows['B'], s_rows['A']]
                    
                    result_df = result_df.append(pd.Series(input_row, index=result_df.columns), ignore_index=True)

                    maf_flag = True

                    break # 세번째 루프를 끝내고 그 다음 maf 포지션으로 가겠다는것 
                # else:
                #     maf_flag = True

        if maf_flag == False: # segment 사잇값 x
            input_row = [':'.join([m_rows['Chromosome'], str(m_rows['Start_Position']), str(m_rows['End_Position'])]), \
                        m_rows['t_ref_count'], m_rows['t_alt_count'], NORMAL_CN, int(0), int(2)]
            result_df = result_df.append(pd.Series(input_row, index=result_df.columns), ignore_index=True)

    f_name = sample_name + '.tsv'
    output_path = os.path.join(output_dir, f_name)

    result_df = result_df.astype({'normal_cn':int, 'minor_cn':int, 'major_cn':int})
    # print(result_df)

    # exit(0)
    result_df.to_csv(output_path, sep='\t', index=False)


    