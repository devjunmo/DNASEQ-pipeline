from glob import glob
import pandas as pd
import os



# 빈 데이터프레임을 만든다. 
# sample_id,total,mean,granular_third_quartile,granular_median,granular_first_quartile,%_bases_above_15 << 헤더


# 데이터 목록 가져서와서
# 샘플 하나마다 루프를 통해 df로 가져오고
# 걔를 샘플 이름을 index로 주고 붙여준다.


# input_dir = r'/myData/DOC_data/WGS/Teratoma_project/' # WGS
# input_dir = r'/myData/DOC_data/WES/Teratoma_project/' # WES
input_dir = r'/data_244/utuc/DOC_results/'

input_format = '*.sample_summary'

output_dir_name = r'merge/'
output_file_name = 'doc_data.xlsx'


df_header = ['total','mean','granular_third_quartile','granular_median','granular_first_quartile','%_bases_above_15']

doc_df = pd.DataFrame(columns=df_header)


input_path_lst = glob(input_dir + input_format)

seq_type = input_path_lst[0].split(r'/')[-1].split('_')[0]


for i in range(len(input_path_lst)):
    input_file = input_path_lst[i]
    # sample_name = input_file.split(r'/')[-1].split(r'.')[0].split('_')[-1]

    sample_doc = pd.read_csv(input_file)

    doc_data = list(sample_doc.iloc[0,])

    sample_name = doc_data.pop(0)

    doc_df.loc[sample_name] = doc_data

    # print(doc_df)
    # break

output_dir = input_dir + output_dir_name
output_path = output_dir + seq_type + '_' + output_file_name

if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)

print(doc_df)

doc_df.to_excel(excel_writer=output_path)