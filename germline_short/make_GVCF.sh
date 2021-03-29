#!/bin/bash -e

if [ $# -lt 7 ]
then
    echo usage: $0 [RefGenome] [output.g.vcf.gz] [input.bam] [interval] [table_path]  [RAM] [seqType]
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


source activate gatk4
gatk --java-options $ram HaplotypeCaller \
    -R $ref_genome \
    -O $outputBam \
    -I $inputBam \
    -L $interval \
    -ERC GVCF \

conda deactivate
