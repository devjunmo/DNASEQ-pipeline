#!/bin/bash -e

if [ $# -lt 7 ]
then
    echo usage: $0 [input.bam] [input.vcf.gz] [ref.fasta] [output.vcf] [interval] [1D/2D] [seqType]
    exit 1
fi

input_bam=$1
input_vcf=$2
ref=$3
output_vcf=$4
interval=$5


case "$6" in
    1D)
        type="reference"
    ;;
    2D)
        type="read_tensor"
    ;;
    *)
        echo "1D, 2D를 설정하시오"
        exit 1
    ;;
esac




if [ "$7" = "WGS" ]; then
    interval= 
fi


gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" CNNScoreVariants \
    -I $input_bam \
    -V $input_vcf \
    -R $ref \
    -O $output_vcf \
    --tensor-type $type \
    -L $interval

