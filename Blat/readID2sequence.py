
# readID.txt 파일을 한줄 한줄 읽어서 qsub을 통해 병렬로 fgrep 실행하고,
# -A 3옵션을 주어 출력한 후, '각각'의 파일명으로 쓴다. (임시파일로 사용예정)
# 파일명의 형태는 myfile.tmp.txt로 줄거임
# 다 만들어지면 merge_tmp_txt.py로 하나의 파일로 만든 후, 임시 파일은 제거


import subprocess as sp
import os


root_dir = r'/data_244/utuc/utuc_gdc/mutect2/blat/utuc3rd/HG1'
input_lst_file_name = r'chr19_12628397.txt'
target_fastq_path = r'/data_244/utuc/utuc_fastq/19S-72988-A10-1_1.fastq.gz'

output_dir_name = input_lst_file_name.split('.')[0]

output_dir_path = os.path.join(root_dir, output_dir_name)


####################### pbs config ########################
pbs_N = "blat.utuc3"
pbs_o = os.path.join(root_dir, "pbs_out_blat")
pbs_j = "oe"
pbs_l_core = 2
###########################################################


if os.path.isdir(output_dir_path) is False:
    os.mkdir(output_dir_path)

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)


input_lst_path = os.path.join(root_dir, input_lst_file_name)


f = open(input_lst_path, mode='r', encoding='utf-8')

lines = f.readlines()

# print(lines)

# zcat 19S-72988-A10-1_1.fastq.gz | fgrep -C 5 A00718:367:HJG5KDSX2:2:1604:29794:18740

for line in lines:
    line = line.strip('\n')
    print(line)

    output_f_name = line.replace(':', '_')
    output_f_name = output_f_name + '.tmp.txt'

    output_path = os.path.join(output_dir_path, output_f_name)
    
    sp.call(f'echo "zcat {target_fastq_path} | fgrep -A 4 {line} >> {output_path}" | qsub \
                        -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)

