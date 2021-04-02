#!/bin/bash -e

if [ $# -lt 5 ]
then
    echo usage: $0 [RefGenome] [output.g.vcf.gz] [input.bam] [interval] [seqType_WGS/WES]
    exit 1
fi


ref_genome=$1
output=$2
inputBam=$3
interval=$4


if [ "$6" = "WGS" ]; then
    interval= 
fi

# contamination data
# max_alternate_alleles, variant_index_parameter, variant_index_type ===> x

# "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx30G"
source activate gatk4
gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx30G" HaplotypeCaller \
    -R $ref_genome \
    -O $output \
    -I $inputBam \
    -L $interval \
    -ERC GVCF \

conda deactivate
