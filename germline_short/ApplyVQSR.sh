#!/bin/bash -e

if [ $# -lt 8 ]
then
    echo usage: $0 [INPUT_VCF] [recal_file] [tranches_file] [OUTPUT_VCF] [seqType] [var_type] [interval] [refGenome]
    exit 1
fi


inputVCF=$1
input_recal=$2
input_tranch=$3
output_VCF=$4
seqType=$5
var_type=$6
interval=$7
refGenome=$8




source activate gatk4

case "$var_type" in
    SNP)
        case "$seqType" in
            WGS)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" ApplyVQSR \
                    -R ${refGenome} \
                    -V ${inputVCF} \
                    -O ${output_VCF} \
                    --truth-sensitivity-filter-level 99.0 \
                    --tranches-file ${input_tranch} \
                    --recal-file ${input_recal} \
                    -mode ${var_type}
            ;;
            WES)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" ApplyVQSR \
                    -R ${refGenome} \
                    -V ${inputVCF} \
                    -O ${output_VCF} \
                    --truth-sensitivity-filter-level 99.0 \
                    --tranches-file ${input_tranch} \
                    --recal-file ${input_recal} \
                    -mode ${var_type} \
                    -L ${interval}
            ;;
            *)
                echo "WGS, WES check"
                exit 1
            ;;
        esac

    ;;
    INDEL)
        case "$seqType" in
            WGS)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms30G -Xmx30G" VariantFiltration \
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

# conda deactivate
