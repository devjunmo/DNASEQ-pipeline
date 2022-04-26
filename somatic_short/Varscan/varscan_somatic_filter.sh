#!/bin/bash -e

if [ $# -lt 2 ]
then
        echo usage: $0 [input] [output]
        exit 1
fi



inputVcf=$1
output=$2


source activate gatk4

varscan somaticFilter $inputVcf \
    --min-coverage 20 \
    --min-reads2 5 \
    --min-strands2 2 \
    --min-var-freq 0.05 \
    --output-file $output

conda deactivate


