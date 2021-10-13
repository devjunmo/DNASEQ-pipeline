import pysam
import os
import pandas as pd



bam_dir = r'/data_244/utuc/utuc_gdc'
# input_bam = r'19S-67257-A1_sorted_deduped_recal.bam' # biopsy
input_bam = r'20S-82978-A5-12_sorted_deduped_recal.bam'

bam_path = os.path.join(bam_dir, input_bam)


bam_obj = pysam.AlignmentFile(bam_path, "rb")

# bam_header = pysam.AlignmentHeader()



read_id_lst = []

for read in bam_obj.fetch('chr11', 533873, 533875): # target point를 잡으려면 (target-1, target)으로..
    print(dir(read))
    break
    if read.is_duplicate is False:
        read_id_lst.append(read.query_name)



print(len(read_id_lst)) # 434

print(len(list(set(read_id_lst)))) # 341
