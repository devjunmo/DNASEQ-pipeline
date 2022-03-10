#!/bin/bash -e

if [ $# -lt 2 ]
then
    echo usage: $0 [INPUT_BAM_FILE] [/path/to/output.bam]
    exit 1
fi

input_bam=$1
output=$2


source activate gatk4


    bam_fname=`echo $input_bam | cut -d '.' -f1`

    echo $bam_fname

    mt_bam_output=${bam_fname}_chrM.bam

    
    gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms10G -Xmx10G" PrintReads \
        -I $input_bam \
        -L chr12 \
        -O $mt_bam_output

