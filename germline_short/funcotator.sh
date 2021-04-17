#!/bin/bash -e

if [ $# -lt 6 ]
then
    echo usage: $0 [refGenome] [input.vcf] [output] [output_format/ VCF or MAF] [data_source_dir] [ref_version]
    exit 1
fi

ref_genome=$1
input=$2
output=$3
output_format=$4
data_source_dir=$5
ref_version=$6


source activate gatk4

gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" Funcotator \
    -R $ref_genome \
    -V $input \
    -O $output \
    --output-file-format $output_format \
    --data-sources-path $data_source_dir \
    --ref-version $ref_version

conda deactivate