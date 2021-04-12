#!/bin/bash -e

if [ $# -lt 6 ]
then
    echo usage: $0 [INPUT_BAM_FILE] [/path/output.bam] [table_path] [RefGenome] [seqType] [interval] 
    exit 1
fi


inputBam=$1
outputBam=$2
table=$3

ref_genome=$4
interval=$6

if [ "$6" = "WGS" ]; then
    interval= 
fi

source activate gatk4
gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" ApplyBQSR \
    -I $inputBam \
    -O $outputBam \
    -R $ref_genome \
    -bqsr $3 \
    -L $interval \
    --use-original-qualities \
    --static-quantized-quals 10 --static-quantized-quals 20 --static-quantized-quals 30 \
    --add-output-sam-program-record \
    --create-output-bam-md5
conda deactivate




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

