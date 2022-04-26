#!/bin/bash -e

if [ $# -lt 4 ]
then
        echo usage: $0 [Normal_pileup] [Tumor_pileup] [output_base] [root_Dir]
        exit 1
fi



normal=$1
tumor=$2
output=$3
root_dir=$4

cd $root_dir

source activate gatk4

varscan somatic $normal $tumor $output

conda deactivate