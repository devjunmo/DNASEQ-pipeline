#!/bin/bash -e

if [ $# -lt 3 ]
then
    echo usage: $0 [input.bam] [output.bam] [THREAD] [readName]
    exit 1
fi

samtools sort -@ $3 -O BAM -o $2 -T sorted_T_$4 $1

 