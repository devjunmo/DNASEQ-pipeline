#!/bin/bash -e


if [ $# -lt 2 ]
then
        echo usage: $0 [path to input.f1r2.tar.gz] [path to output.rom.tar.gz]
        exit 1
fi



input=$1
output=$2


source activate gatk4

gatk LearnReadOrientationModel\
	-I "$input" \
	-O "$output"

conda deactivate