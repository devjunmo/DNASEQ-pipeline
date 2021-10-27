#!/bin/bash -e

if [ $# -lt 7 ]
then
    echo usage: $0 [RefGenome] [output.g.vcf.gz OR output.vcf.gz] [input.bam] [interval] [seqType: WGS/WES] [mode: gvcf or single] [bamout]
    exit 1
fi


ref_genome=$1
output=$2
inputBam=$3
interval=$4
bamout=$7


if [ "$5" = "WGS" ]; then
    interval= 
fi

# contamination data
# max_alternate_alleles, variant_index_parameter, variant_index_type ===> x

# "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx30G"

source activate gatk4

case "$5" in
    WGS)
        case "$6" in
            gvcf)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx50G" HaplotypeCaller \
                    -R $ref_genome \
                    -O $output \
                    -I $inputBam \
                    -ERC GVCF
            ;;
            single)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx50G" HaplotypeCaller \
                    -R $ref_genome \
                    -O $output \
                    -I $inputBam \
                    --bam-output $bamout
            ;;
            *)
                echo "mode를 확인하시오 gvcf or single 입력"
                exit 1
            ;;
        esac
    ;;
    WES)
        case "$6" in
            gvcf)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx20G" HaplotypeCaller \
                    -R $ref_genome \
                    -O $output \
                    -I $inputBam \
                    -L $interval \
                    -ERC GVCF
            ;;
            single)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx20G" HaplotypeCaller \
                    -R $ref_genome \
                    -O $output \
                    -I $inputBam \
                    -L $interval \
                    --bam-output $bamout
            ;;
            *)
                echo "mode를 확인하시오 gvcf or single 입력"
                exit 1
            ;;
        esac
    ;;
    *)
        echo "seq type확인, WES or WGS"
        exit 1
    ;;
esac


# conda deactivate