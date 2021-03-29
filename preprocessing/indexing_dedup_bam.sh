#!/bin/bash -e

if [ $# -lt 2 ]
then
    echo usage: $0 [thread] [output_name.bam]
    exit 1
fi


samtools index -@ $1 $2