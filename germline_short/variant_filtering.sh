#!/bin/bash -e

if [ $# -lt 4 ]
then
    echo usage: $0 [input_raw_vcf] [select_type] [output_selected_vcf] [output_filtered_vcf]
    exit 1
fi

raw_vcf = $1
select_type = $2
selected_vcf = $3
filtered_vcf = $4


if [ "$7" = "WGS" ]; then
    interval= 
fi

# contamination data
# max_alternate_alleles, variant_index_parameter, variant_index_type ===> x

# "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx80G"


source activate gatk4

gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" SelectVariants \
    -V $raw_vcf \
    -select-type $select_type \
    -O $selected_vcf


gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" VariantFiltration \
    -V $selected_vcf \
    -filter "QD < 2.0" --filter-name "QD2" \
    -filter "FS > 30.0" --filter-name "FS30" \
    -filter "SOR > 3.0" --filter-name "SOR3" \
    -filter "MQ < 40.0" --filter-name "MQ40" \
    -filter "MQRankSum < -3.0" --filter-name "MQRankSum-3.0" \
    -filter "ReadPosRankSum < -3.0" --filter-name "ReadPosRankSum-3" \
    -filter "QUAL < 30.0" --filter-name "QUAL30" \
    -O $filtered_vcf

conda deactivate

