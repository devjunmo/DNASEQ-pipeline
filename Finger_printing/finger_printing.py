import pandas as pd
import natsort
import os
from glob import glob
import numpy as np


pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)


input_dir = r'E:/stemcell/finger_print/VCF'
output_dir_name = r'FP_output'
# col: Tumor / Normal로 세팅
pair_info_csv = r'E:/stemcell/finger_print/stemcell_WES_sample_pair_220117.csv'
output_dir = os.path.join(input_dir, output_dir_name)
output_path = os.path.join(output_dir, 'stemcell_WES_fingerprint.xlsx')


class FingerPrint():

    def __init__(self, _vcf_dir, _output_dir, _pair_info_path):
        self.vcf_list = glob(os.path.join(_vcf_dir, '*.vcf'))
        self.out_dir = _output_dir
        self.pair_dict = self.__make_pair_dict(_pair_info_path)
        self.mut_id_lst = self.__make_mutation_id_lst(self.vcf_list)
        self.finger_print_df = self.__make_finger_print_empty_df(
            self.vcf_list, self.mut_id_lst, self.pair_dict)
        self.finger_print_df = self.__run_finger_print(
            self.finger_print_df, self.vcf_list)

    def __make_pair_dict(self, _pair_info):
        pair_df = pd.read_csv(_pair_info)
        # {tumor : {normal:_ grade:_} dict 형태
        pair_df.set_index('Tumor', inplace=True)
        return pair_df.to_dict('index')

    def __make_mutation_id_lst(self, _vcf_list):
        mut_id_lst = []
        for i in range(len(_vcf_list)):
            vcf_df = self.__vcf_setting(_vcf_list[i])
            mut_id_tmp_lst = vcf_df['mut_id'].to_list()
            mut_id_lst = mut_id_lst + mut_id_tmp_lst
        mut_id_lst = list(set(mut_id_lst))  # unique 효과
        mut_id_lst.sort()

        return mut_id_lst

    def __make_finger_print_empty_df(self, _vcf_list, _mutation_id_lst, _pair_dict):
        sample_name_lst_for_idx = []
        sample_name_lst = []
        for i in range(len(_vcf_list)):
            vcf_df = self.__vcf_setting(_vcf_list[i])
            sample_name = vcf_df.columns.tolist()[-2]
            sample_name_lst.append(sample_name)
            try:
                _normal = _pair_dict[sample_name]['Normal']
            except KeyError:
                _normal = 'NaN'
            sample_name = sample_name + f'_[origin: {_normal}]'
            sample_name_lst_for_idx.append(sample_name)
        # empty df 생성
        _fp_df = pd.DataFrame(index=sample_name_lst_for_idx,
                              columns=_mutation_id_lst)
        _fp_df['sample'] = sample_name_lst
        # print(_fp_df)
        return _fp_df

    def __run_finger_print(self, _empty_fp_df, _vcf_list):
        for i in range(len(_vcf_list)):
            vcf_df = self.__vcf_setting(_vcf_list[i])
            # print(vcf_df)
            mut_id_tmp_lst = vcf_df['mut_id'].to_list()
            filter_tmp_lst = vcf_df['ALT'].to_list()
            mutid_info_dict = dict(zip(mut_id_tmp_lst, filter_tmp_lst))
            # print(mutid_info_dict)
            # mutid_dict => {mutid : pass, mutid2:SOR ...}
            sample_name = vcf_df.columns.tolist()[-2]
            # print(_empty_fp_df)
            _idx = _empty_fp_df[_empty_fp_df['sample'] == sample_name].index
            # print(type(_empty_fp_df[_empty_fp_df['sample'] == sample_name]))
            # _empty_fp_df.loc[_idx, 'chr4_72750280'] = 100
            # print(_empty_fp_df)

            for _mutID, _alt in mutid_info_dict.items():
                # print(_mutID, _filter)
                _empty_fp_df.loc[_idx, _mutID] = _alt
                # print(_empty_fp_df)
            # exit(0)

        return _empty_fp_df

    def __vcf_setting(self, _vcf_path):
        vcf_df = pd.read_csv(_vcf_path, sep='\t')
        vcf_df['POS'] = vcf_df['POS'].astype(str)
        vcf_df['mut_id'] = vcf_df['#CHROM'] + '_' + vcf_df['POS']
        return vcf_df


if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


finger_print_obj = FingerPrint(input_dir, output_dir, pair_info_csv)

finger_print_df = finger_print_obj.finger_print_df

print(finger_print_df)

# finger_print_df.to_csv(output_path, header=True,
#                        index=True, quoting=False, na_rep='NaN')
print(os.getcwd())
finger_print_df.to_excel(output_path, na_rep='NaN', header=True, index=True)