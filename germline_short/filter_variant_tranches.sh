#!/bin/bash -e

if [ $# -lt 5 ]
then
    echo usage: $0 [input.vcf] [output.vcf] [interval] [1D/2D] [seqType]
    exit 1
fi


input_vcf=$1
output_vcf=$2
interval=$3

resource_hapmap='/data_244/refgenome/b37/hapmap_3.3.b37.vcf'
resource_mills='/data_244/refgenome/b37/Mills_and_1000G_gold_standard.indels.b37.vcf'


case "$4" in
    1D)
        key="pass"
    ;;
    2D)
        key="CNN_2D"
    ;;
    *)
        echo "1D, 2D를 설정하시오"
        exit 1
    ;;
esac


if [ "$5" = "WGS" ]; then
    interval= 
fi


gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" FilterVariantTranches \
    -V $input_vcf \
    --resource $resource_hapmap \
    --resource $resource_mills \
    --info-key $key \
    --snp-tranche 99.95 \
    --indel-tranche 99.4 \
    --invalidate-previous-filters \
    -O $output_vcf \
    -L $interval

