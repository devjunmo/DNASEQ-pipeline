#!/bin/bash -e

if [ $# -lt 3 ]
then
    echo usage: $0 [input_name.sam] [output_name.bam] [thread]
    exit 1
fi


samtools view -Sb -h -@ $3 $1 -o $2

sleep 20s