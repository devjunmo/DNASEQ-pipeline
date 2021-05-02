#!/bin/bash -e

if [ $# -lt 6 ]
then
    echo usage: $0 [refGenome] [input.vcf.gz] [output.vcf.gz] [select_type] [seqType] [interval]
    exit 1
fi

refGenome=$1
input_vcf=$2
output_vcf=$3

interval=$6


case "$4" in
    SNP)
        type="SNP"
    ;;
    INDEL)
        type="INDEL"
    ;;
    *)
        echo "select SNP, INDEL"
        exit 1
    ;;
esac



source activate gatk4

case "$5" in
    WGS)
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" SelectVariants \
            -R $refGenome \
            -V $input_vcf \
            -select-type $type \
            -O $output_vcf
    ;;
    WES)
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" SelectVariants \
            -R $refGenome \
            -V $input_vcf \
            -select-type $type \
            -O $output_vcf \
            -L $interval
    ;;
    *)
        echo "seqType=WES, WGS"
        exit 1
    ;;
esac

# conda deactivate