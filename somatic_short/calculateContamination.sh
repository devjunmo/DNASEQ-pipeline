#!/bin/bash -e


if [ $# -lt 3 ]
then
        echo usage: $0 [path to input.getpileupsummaries.table] [path to out.segments.table] [path to output.calculatecontamination.table]
        exit 1
fi



input=$1
seg_table=$2
output=$3


source activate gatk4

gatk CalculateContamination \
	-I "$input" \
	-tumor-segmentation "$seg_table" \
	-O "$output"

conda deactivate