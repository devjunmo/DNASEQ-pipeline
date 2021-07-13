#!/bin/bash -e


if [ $# -lt 3 ]
then
        echo usage: $0 [tumor bam path] [SEC path] [output.getpileupsummaries.table path]
        exit 1
fi



tumor=$1
sec=$2
output=$3


source activate gatk4

gatk GetPileupSummaries \
	-I "$tumor" \
	-V "$sec" \
	-L "$sec" \
	-O "$output"

conda deactivate