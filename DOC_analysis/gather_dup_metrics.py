from glob import glob
import pandas as pd
import os


# input_dir = r'E:/DOC_data/WES/Teratoma_project/dup_metrics/'
input_dir = r'E:/DOC_data/WGS/Teratoma_project/dup_rate/'

input_format = '*.txt'

output_dir_name = r'merge/'
output_file_name = 'dup_rate.xlsx'


# df_header = ['LIBRARY', 'UNPAIRED_READS_EXAMINED', 'READ_PAIRS_EXAMINED', 'SECONDARY_OR_SUPPLEMENTARY_RDS', 'UNMAPPED_READS', \
#                 'UNPAIRED_READ_DUPLICATES', 'READ_PAIR_DUPLICATES', 'READ_PAIR_OPTICAL_DUPLICATES', 'PERCENT_DUPLICATION', 'ESTIMATED_LIBRARY_SIZE']

# doc_df = pd.DataFrame(columns=df_header)

df_header = ['PERCENT_DUPLICATION']

dup_df = pd.DataFrame(columns=df_header)


input_path_lst = glob(input_dir + input_format)

seq_type = input_path_lst[0].split(r'/')[-1].split('_')[0]


for i in range(len(input_path_lst)):
    input_file = input_path_lst[i]
    # sample_name = input_file.split(r'/')[-1].split(r'.')[0].split('_')[-1]

    sample_dup = pd.read_csv(input_file)

    print(sample_dup.iloc[0, 0])
    print(type(sample_dup.iloc[0, 0]))

    dup_data = sample_dup.iloc[0, 0]
    dup_data = dup_data.split()
    
    per_dup_data = dup_data[-2]
    sample_name = dup_data[0]


    # dup_data = list(sample_dup.iloc[0,])
    # # print(doc_data)
    # # exit()

    # sample_name = dup_data.pop(0)

    dup_df.loc[sample_name] = per_dup_data
    # exit(0)

    # print(doc_df)
    # break

output_dir = input_dir + output_dir_name
output_path = output_dir + seq_type + '_' + output_file_name

if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)

print(dup_df)

# doc_df = dup_df.loc[:, ['total', 'mean']]
# # print(type(doc_df))

# del doc_df['total']
# print(doc_df)


# exit(0)

dup_df.to_excel(excel_writer=output_path)