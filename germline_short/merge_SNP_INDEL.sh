#!/bin/bash -e

if [ $# -lt 3 ]
then
    echo usage: $0 [snp_vcf] [indel_vcf] [output_path]
    exit 1
fi



SNP=$1
INDEL=$2
output_path=$3



source activate gatk4

gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms3G -Xmx3G" MergeVcfs \
    -I $SNP \
    -I $INDEL \
    -O $output_path