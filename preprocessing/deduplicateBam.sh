#!/bin/bash -e

if [ $# -lt 4 ]
then
    echo usage: $0 [INPUT_BAM_FILE] [/path/to/output.bam] [sorting_order] [metricPrefix]
    exit 1
fi

input=$1
output=$2
patterned=2500



source activate gatk4
    gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms30G -Xmx30G" MarkDuplicates \
        -I $input \
        -O $output \
        --METRICS_FILE $4marked_dup_metrics.txt \
        --VALIDATION_STRINGENCY SILENT \
        --OPTICAL_DUPLICATE_PIXEL_DISTANCE $patterned \
        --CREATE_MD5_FILE true \
        --ASSUME_SORT_ORDER $3
conda deactivate

sleep 30s
