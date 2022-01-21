import os
from glob import glob


# input_path_list 가져오기

def get_input_path_list(_input_dir, _input_format, _is_print):
    input_lst = glob(os.path.join(_input_dir, _input_format))
    if _is_print:
        print(input_lst)
    return input_lst

# wd에 output_dir 만들기
def set_output_dir(_root_dir, _output_dir_name):
    output_dir = os.path.join(_root_dir, _output_dir_name)
    if os.path.isdir(output_dir) is False:
        os.mkdir(output_dir)

