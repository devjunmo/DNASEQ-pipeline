

from SigProfilerMatrixGenerator import install as genInstall
from SigProfilerExtractor import sigpro as sig
import os
import subprocess as sp
from glob import glob


# 각각의 폴더로 진행

if __name__ == '__main__':

    old_wd = os.getcwd()

    root_dir = r'/home/jun9485/data/utuc/somatic_call/filtered/vcf/'
    vcf_format = '*.vcf'
    vcf_dir_format = r'filtered*'

    vcf_lst = glob(root_dir + vcf_format)

    for i in range(len(vcf_lst)):
        vcf_file = vcf_lst[i]
        sample_name = vcf_file.split(r'/')[-1].split('.')[0]
        mk_dir_path = root_dir + sample_name
        
        if os.path.isdir(mk_dir_path) is False:
            os.mkdir(mk_dir_path)
            sp.call(rf'cp {vcf_file} {mk_dir_path}', shell=True)


    # exit(0)

    os.chdir(root_dir)

    # os.getcwd()


    # input_vcf_dir = '/home/jun9485/data/utuc/somatic_call/filtered/snp/'

    # path_to_example_table = sig.importdata("vcf")

    # path_to_example_table = sig.importdata("vcf")
    # print(path_to_example_table)


    input_dir_lst = glob(root_dir + vcf_dir_format)

    # print(input_dir_lst)


    for i in range(len(input_dir_lst)):

        input_vcf_dir = input_dir_lst[i]
        input_vcf_dir_name = input_vcf_dir.split(r'/')[-1]

        out_dir_name = rf'sig_analysis_{input_vcf_dir_name}/'

        sig.sigProfilerExtractor('vcf', out_dir_name, input_vcf_dir)
