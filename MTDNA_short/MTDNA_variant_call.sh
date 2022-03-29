#!/bin/bash -e

if [ $# -lt 4 ]
then
    echo usage: $0 [INPUT_BAM_FILE] [/path/to/output.bam] [Ref.genome] [tmp.pss.bam]
    exit 1
fi

input_bam=$1
output=$2
refGenome=$3


source activate gatk4


    bam_fname=`echo $input_bam | cut -d '.' -f1`
    mt_bam_output=${bam_fname}_chrM.bam # mt-bam

    
    PrintReads
    gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms10G -Xmx10G" PrintReads \
        -I $input_bam \
        -L chrM \
        -O $mt_bam_output

    
    mt_bam_fname=`echo $mt_bam_output | cut -d '.' -f1`
    qsort_mt_bam_output=${mt_bam_fname}_Qsorted.bam # Qsorted-mt-bam


    # SortSam
    gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms10G -Xmx10G" SortSam \
        -I $mt_bam_output \
        --SORT_ORDER queryname \
        -O $qsort_mt_bam_output
    
    
    # # bam processing...


    qs_mt_bam_fname=`echo $qsort_mt_bam_output | cut -d '.' -f1`
    revert_qs_mt_bam_output=${qs_mt_bam_fname}_revert.bam # mt-revert-bam


    # # RevertSam
    gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms10G -Xmx10G" RevertSam \
        -I $qsort_mt_bam_output \
        -O $revert_qs_mt_bam_output \
        --SANITIZE true
    # gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms10G -Xmx10G" RevertSam \
    #     -I $4 \
    #     -O $revert_qs_mt_bam_output \
    #     --SANITIZE true


    rv_qs_mt_bam_fname=`echo $revert_qs_mt_bam_output | cut -d '.' -f1`
    merged_rv_qs_mt_bam_output=${rv_qs_mt_bam_fname}_merged.bam

    processed_aligned_bam=${qs_mt_bam_fname}_processed.bam # mt-revert-bam



    # MergeBamAlignment
    # gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms50G -Xmx50G" MergeBamAlignment \
    #     --UNMAPPED_BAM $revert_qs_mt_bam_output \
    #     --ALIGNED_BAM $qsort_mt_bam_output \
    #     -O $merged_rv_qs_mt_bam_output \
    #     -R $refGenome
    gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms50G -Xmx50G" MergeBamAlignment \
        --UNMAPPED_BAM $revert_qs_mt_bam_output \
        --ALIGNED_BAM $4 \
        -O $merged_rv_qs_mt_bam_output \
        -R $refGenome

