#!/bin/bash -e

if [ $# -lt 8 ]
then
        echo usage: $0 [tumor_bam] [normal_bam] [target] [fasta] [access] [outref] [resultDir] [thread]
        exit 1
fi

tumor=$1
normal=$2
target=$3
refGenome=$4
access=$5
outref=$6
resultDir=$7
thread=$8




source activate gatk4

cnvkit.py batch $tumor --normal $normal \
    --targets $target \
    --fasta $refGenome \
    --access $access \
    --output-reference $outref --output-dir $resultDir \
    --diagram --scatter -p $thread

conda deactivate