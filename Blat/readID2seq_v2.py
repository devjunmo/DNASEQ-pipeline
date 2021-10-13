"""

#   input 형식
#   [HG1 chr start end]
#   @RAD:fadvksa:351
#   @ASDF:dga:asdf:123
#   [HG2 chr start end]
#   @~~~~

 위 형식을 받아서 {'[HG1 chr start end]':['@RAD:fadvksa:351', @ASDF:dga:asdf:123], 
                   '[HG2 chr start end]':['@~~~', ...]}

 이것과 같은 딕셔너리를 만들고, 정렬한다음
 파일에 쓴다. 
 아웃풋 파일 형식은

 [HG1 chr start end]
 @RAD:fadvksa:351
 ATTCGTATCT
 +
 FFFFFFFFFF
 @ASDF:dga:asdf:123
 ACCGATGTCT
 +
 FFFFFFFFFF
 (공백 주면 좋다)
 [HG2 chr start end]

 이런 형태가 될것
 
"""





import subprocess as sp
import os


# root_dir = r'/data_244/utuc/utuc_gdc/mutect2/blat/utuc3rd/whole'
root_dir = r'/data_244/utuc/utuc_gdc/mutect2/blat/utuc2nd/whole'


# input_lst_file_name = r'utuc_3rd_readID_data_for_blat.txt'
input_lst_file_name = r'utuc_2nd_readID_data_for_blat_1.txt'

fastq_dir = r'/data_244/utuc/utuc_fastq'

is_using_qsub = True

# # utuc_3rd
# fastq_dict = {'Biopsy1': os.path.join(fastq_dir, '19S-67257-A1_1.fastq.gz'),
#                 'HG1': os.path.join(fastq_dir, '19S-72988-A10-1_1.fastq.gz'),
#                 'HG2': os.path.join(fastq_dir, '19S-72988-A10-2_1.fastq.gz'),
#                 'LG1': os.path.join(fastq_dir, '19S-72988-A10-3_1.fastq.gz'),
#                 'LG2': os.path.join(fastq_dir, '19S-72988-A10-4_1.fastq.gz'),
#                 'INT1': os.path.join(fastq_dir, '19S-72988-A10-5_1.fastq.gz'),
#                 'INT2': os.path.join(fastq_dir, '19S-72988-A10-6_1.fastq.gz')}

# utuc_2rd
fastq_dict = {'HG1': os.path.join(fastq_dir, '20S-82978-A2-8_1.fastq.gz'),
                'HG2': os.path.join(fastq_dir, '20S-82978-A3-10_1.fastq.gz'),
                'LG2': os.path.join(fastq_dir, '20S-82978-A3-15_1.fastq.gz'),
                'LG1': os.path.join(fastq_dir, '20S-82978-A5-12_1.fastq.gz'),
                'INT1': os.path.join(fastq_dir, '20S-82978-A5-13_1.fastq.gz')}

# output_name = 'utuc_3rd_seq_for_blat_1.txt'
output_name = 'utuc_2nd_seq_for_blat_1.txt'

output_path = os.path.join(root_dir, output_name)


####################### pbs config ########################
pbs_N = "blat.utuc2"
pbs_o = os.path.join(root_dir, "pbs_out_blat")
pbs_j = "oe"
pbs_l_core = 2
###########################################################


# if os.path.isdir(output_dir_path) is False:
#     os.mkdir(output_dir_path)

if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)


input_lst_path = os.path.join(root_dir, input_lst_file_name)


f = open(input_lst_path, mode='r', encoding='utf-8')

lines = f.readlines()

f.close()

head_idx_lst = []

line_count = 0

for line in lines:
    line = line.strip('\n')
    # print(line[0])

    if line[0] == '[':
        head_idx_lst.append(line_count)
    line_count += 1

head_idx_lst.append(len(lines)) # [헤더1 idx, 헤더2 idx, ..., last_idx + 1]


for i in range(len(head_idx_lst) - 1):
    header = lines[head_idx_lst[i]].strip('\n')
    seq_data = lines[head_idx_lst[i]+1:head_idx_lst[i+1]]
    seq_data = [sd.rstrip('\n') for sd in seq_data]

    header_data = header.strip('[]')
    sample = header_data.split(' ')[0]
    target_fastq = fastq_dict[sample]


    if is_using_qsub is False:

        sp.call(rf'echo {header} >> {output_path}', shell=True)

        for data in seq_data:
            sp.call(rf'zcat {target_fastq} | fgrep -A 3 {data} >> {output_path}', shell=True)

    else:

        header_data = header_data.replace(' ', '_')
        output_dir_path = os.path.join(root_dir, header_data)

        if os.path.isdir(output_dir_path) is False:
            os.mkdir(output_dir_path)

        output_name_qsub = header_data + '.txt'
        output_path_qsub = os.path.join(output_dir_path, output_name_qsub)

        for data in seq_data:    
            sp.call(f'echo "zcat {target_fastq} | fgrep -A 3 {data} >> {output_path_qsub}" | qsub \
                                -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)





# for i in range(len(head_idx_lst) - 1):
#     header = lines[i].strip('\n')
#     seq_data = lines[i+1:head_idx_lst[i+1]-1]
#     seq_data = [sd.rstrip('\n') for sd in seq_data]

#     header_data = header.strip('[]')
#     sample = header_data.split(' ')[0]
#     target_fastq = fastq_dict[sample]

#     sp.call(rf'echo {header} >> {output_path}', shell=True)

#     for data in seq_data:
#         sp.call(rf'zcat {target_fastq} | fgrep -A 3 {data} >> {output_path}', shell=True)






# for line in lines:
#     line = line.strip('\n')
#     # print(line[0])

#     if line[0] == '[':
#         pass

#     break

#     output_f_name = line.replace(':', '_')
#     output_f_name = output_f_name + '.tmp.txt'

#     output_path = os.path.join(output_dir_path, output_f_name)
    
#     sp.call(f'echo "zcat {target_fastq_path} | fgrep -A 3 {line} >> {output_path}" | qsub \
#                         -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)

