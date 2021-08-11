

# Vardict-java의 필터가 제대로 적용되지 않아서 시도하는 코드

import os
from glob import glob
import subprocess as sp


input_dir = r'/data_244/stemcell/WES/ips_recal_bam/vardict_tumor_only/problems'
input_format = '*.vcf'

output_dir_name = r're_filter_VCF'
output_dir = os.path.join(input_dir, output_dir_name)

GATK_PATH = '/home/pbsuser/bin/gatk'

if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)


input_vcf_lst = glob(os.path.join(input_dir, input_format))

print(input_vcf_lst)

for input_vcf in input_vcf_lst:
    print(input_vcf)

    sample_name = input_vcf.split(r'/')[-1].split(r'.')[0].split(r'_')[-1]

    output_name = sample_name + '_vardict_new-Filter.vcf'

    output_path = os.path.join(output_dir, output_name)

    sp.call(f'{GATK_PATH} --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms30G -Xmx30G" VariantFiltration\
                    -V {input_vcf} -O {output_path} \
                    -filter "QUAL < 30.0" --filter-name "QUAL30" \
                    -filter "MQ < 30.0" --filter-name "MQ30" \
                    -filter "VD < 5" --filter-name "VD5" \
                    -filter "DP < 30" --filter-name "DP30" \
                    -filter "PMEAN < 8.0" --filter-name "PMEAN8" \
                    -filter "SN < 1.5" --filter-name "SN1.5" \
                    -filter "PSTD == 0" --filter-name "PSTD0" \
                    -filter "AF < 0.05" --filter-name "AF0.05" \
                    -filter "NM >= 5.25" --filter-name "NM5.25"', shell=True)

