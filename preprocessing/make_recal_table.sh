#!/bin/bash -e

if [ $# -lt 6 ]
then
    echo usage: $0 [INPUT_BAM_FILE] [/path/output.table] [RefGenome] [RefGenomeDir] [seqType] [interval]
    exit 1
fi


input=$1
output=$2
ref_genome=$3
ref_dir=$4
interval=$6

ks_dbSNP=$ref_dir"dbsnp_138.b37.vcf"
ks_mills=$ref_dir"Mills_and_1000G_gold_standard.indels.b37.vcf"
ks_1000G=$ref_dir"1000G_phase1.indels.b37.vcf"


case "$5" in
    "WES")
        source activate gatk4
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" BaseRecalibrator \
            -I $input \
            -O $output \
            --known-sites $ks_dbSNP \
            --known-sites $ks_mills \
            --known-sites $ks_1000G \
            -R $ref_genome \
            --use-original-qualities \
            -L $interval
        conda deactivate
    ;;
    "WGS")
        source activate gatk4
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" BaseRecalibrator \
            -I $input \
            -O $output \
            --known-sites $ks_dbSNP \
            --known-sites $ks_mills \
            --known-sites $ks_1000G \
            -R $ref_genome \
            --use-original-qualities \
        conda deactivate
    ;;
    *)
        echo "seqType = WES or WGS"
        exit 1
    ;;
esac

sleep 20s
