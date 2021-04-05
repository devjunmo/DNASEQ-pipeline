#!/bin/bash -e

if [ $# -lt 5 ]
then
    echo usage: $0 [INPUT_BAM_FILE] [/path/to/output.bam] [IsRmDupInOutput] [RAM] [metricPrefix]
    exit 1
fi

input=$1
output=$2
isRm=$3
ram="-Xmx"$4"G"
patterned=2500


case "$3" in
    True)
        source activate gatk4
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx10G" MarkDuplicates \
            -I $input \
            -O $output \
            --METRICS_FILE $5marked_dup_metrics.txt \
            --remove-sequencing-duplicates \
            --VALIDATION_STRINGENCY SILENT \
            --OPTICAL_DUPLICATE_PIXEL_DISTANCE $patterned \
            --CREATE_MD5_FILE true
            --ASSUME_SORT_ORDER "queryname"
        conda deactivate
    ;;
    False)
        source activate gatk4
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx10G" MarkDuplicates \
            -I $input \
            -O $output \
            --METRICS_FILE $5marked_dup_metrics.txt \
            --VALIDATION_STRINGENCY SILENT \
            --OPTICAL_DUPLICATE_PIXEL_DISTANCE $patterned \
            --CREATE_MD5_FILE true
            --ASSUME_SORT_ORDER "queryname"
        conda deactivate
    ;;
    *)
        echo "IsRmDupInOutput 인자에 True or False를 입력하시오"
        exit 1
    ;;
esac

