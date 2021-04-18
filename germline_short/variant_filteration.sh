#!/bin/bash -e

if [ $# -lt 5 ]
then
    echo usage: $0 [input.vcf.gz] [output.vcf.gz] [select_type] [seqType] [interval]
    exit 1
fi


input_vcf=$1
output_vcf=$2
type=$3
interval=$5


source activate gatk4

case "$type" in
    SNP)
        case "$4" in
            WGS)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" VariantFiltration \
                    -V $input_vcf \
                    -filter "QD < 2.0" --filter-name "QD2" \
                    -filter "QUAL < 30.0" --filter-name "QUAL30" \
                    -filter "SOR > 3.0" --filter-name "SOR3" \
                    -filter "FS > 60.0" --filter-name "FS60" \
                    -filter "MQ < 40.0" --filter-name "MQ40" \
                    -filter "MQRankSum < -12.5" --filter-name "MQRankSum-12.5" \
                    -filter "ReadPosRankSum < -8.0" --filter-name "ReadPosRankSum-8" \
                    -O $output_vcf
            ;;
            WES)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" VariantFiltration \
                    -V $input_vcf \
                    -filter "QD < 2.0" --filter-name "QD2" \
                    -filter "QUAL < 30.0" --filter-name "QUAL30" \
                    -filter "SOR > 3.0" --filter-name "SOR3" \
                    -filter "FS > 60.0" --filter-name "FS60" \
                    -filter "MQ < 40.0" --filter-name "MQ40" \
                    -filter "MQRankSum < -12.5" --filter-name "MQRankSum-12.5" \
                    -filter "ReadPosRankSum < -8.0" --filter-name "ReadPosRankSum-8" \
                    -L $interval \
                    -O $output_vcf
            ;;
            *)
                echo "WGS, WES check"
                exit 1
            ;;
        esac

    ;;
    INDEL)
        case "$4" in
            WGS)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" VariantFiltration \
                    -V $input_vcf \
                    -filter "QD < 2.0" --filter-name "QD2" \
                    -filter "QUAL < 30.0" --filter-name "QUAL30" \
                    -filter "FS > 200.0" --filter-name "FS200" \
                    -filter "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20" \
                    -O $output_vcf
            ;;
            WES)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" VariantFiltration \
                    -V $input_vcf \
                    --filter "QD < 2.0" --filter-name "QD2" \
                    -filter "QUAL < 30.0" --filter-name "QUAL30" \
                    -filter "FS > 200.0" --filter-name "FS200" \
                    -filter "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20" \
                    -L $interval \
                    -O $output_vcf
            ;;
            *)
                echo "WGS, WES check"
                exit 1
            ;;
        esac
    ;;
    *)
        echo "SNP, INDEL check"
        exit 1
    ;;
esac

conda deactivate
