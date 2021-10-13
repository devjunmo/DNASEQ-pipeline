import pysam
import os
import pandas as pd



bam_dir = r'/data_244/utuc/utuc_gdc'
input_bam = r'19S-67257-A1_sorted_deduped_recal.bam' # biopsy
# input_bam = r'20S-82978-A3-15_sorted_deduped_recal.bam'

bam_path = os.path.join(bam_dir, input_bam)


bam_obj = pysam.AlignmentFile(bam_path, "rb")

# bam_header = pysam.AlignmentHeader()


count = 0
for read in bam_obj.fetch('chr11', 533873, 533874): # target point를 잡으려면 (target-1, target)으로..
    count += 1
    print(read)
    print(type(read))

    # print(dir(read))
    print(read.query_name)
    print(type(read.query_name))
    print(read.is_duplicate)
    break

# print(count)


# for pileupcolumn in bam_obj.pileup('chr11', 478916, 478917):
#     print ("\ncoverage at base %s = %s" %
#            (pileupcolumn.pos, pileupcolumn.n))
#     for pileupread in pileupcolumn.pileups:
#         if not pileupread.is_del and not pileupread.is_refskip:
#             # query position is None if is_del or is_refskip is set.
#             print ('\tbase in read %s = %s' %
#                   (pileupread.alignment.query_name,
#                    pileupread.alignment.query_sequence[pileupread.query_position]))