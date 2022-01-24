
import seaborn as sns
import os
from random import sample
from turtle import shape
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.getcwd(), 'jun_tools'))
import jun_mtd

input_dir = r'E:/stemcell/mouse_mapping/flagstat'
input_format = r'*.tsv'
output_dir_name = r'results'

output_dir = jun_mtd.set_output_dir(input_dir, output_dir_name)

for_plotting_data_path = os.path.join(output_dir, 'trimmed_mapping_rate.csv')

out_csv_path = os.path.join(output_dir, 'mapping_rate_rbind.csv')

input_lst = jun_mtd.get_input_path_list(input_dir, input_format, False)


class CheckMappingRate():

    def __init__(self, input_list, out_csv_path) -> None:
        self.input_lst = input_list
        self.out_df = np.NaN
        self.__rbind_mapping_data()
        self.__saving_mapping_df(out_csv_path)

    def __data_preprocessing(self, _raw_tsv_path):
        sample_name = jun_mtd.get_f_name(_raw_tsv_path).split(r'.')[
            0].split('_')[0]
        tmp_df = pd.read_csv(_raw_tsv_path, sep='\t')
        tmp_dt = tmp_df.transpose()
        tmp_dt = tmp_dt.reset_index()
        tmp_dt = tmp_dt.rename(columns=tmp_dt.iloc[2])
        tmp_dt = tmp_dt.drop(tmp_dt.index[2])
        tmp_col_names = tmp_dt.columns.tolist()
        tmp_col_names = ['sample'] + tmp_col_names
        tmp_dt['sample'] = sample_name
        tmp_dt = tmp_dt[tmp_col_names]
        # df_for_pot = tmp_dt.loc[0:0]
        # print(tmp_dt.loc[0:0])
        return tmp_dt

    def __rbind_mapping_data(self):
        for i in range(len(input_lst)):
            input_df = self.__data_preprocessing(input_lst[i])
            if self.out_df is np.NaN:
                self.out_df = input_df
                # print(self.out_df)
            else:
                self.out_df = pd.concat([self.out_df, input_df])

    def __saving_mapping_df(self, _out_path):
        self.out_df.to_csv(_out_path, index=False, header=True, na_rep='NaN')
        dropped_df = self.out_df.drop(index=1)
        _out_path2 = os.path.join(os.path.split(
            _out_path)[0], 'trimmed_mapping_rate.csv')
        if os.path.isfile(_out_path2) is False:
            print('making dataframe for plotting')
            dropped_df.to_csv(_out_path2, index=False,
                              header=True, na_rep='NaN')

    @classmethod
    def plotting_mapping_data(cls, _df, _group_col_name):
        print(_df)
        # plt.scatter(_df['sample'], _df['mapped %'], c=_df[_group_col_name], edgecolors='black',
        #             cmap='Reds_r', linewidths=1)
        # plt.xticks(rotation=-90)
        # plt.grid(axis='y', linestyle='--')
        # plt.show()
        sns.set(font_scale=1)
        _df_s = _df.sort_values(by=['mapped %'], ascending=[False])

        sns.scatterplot(x='sample', y='mapped %',
                        hue=_group_col_name, style=_group_col_name,
                        s=100, data=_df_s)
        plt.xticks(rotation=-90)
        plt.grid(axis='both', linestyle='--')
        plt.legend(loc=1, prop={'size': 30})

        plt.show()
        exit(0)


if __name__ == '__main__':

    check_mapping_rate_obj = CheckMappingRate(input_lst, out_csv_path)

    for_plotting_df = pd.read_csv(for_plotting_data_path)
    CheckMappingRate.plotting_mapping_data(for_plotting_df, 'grp')
