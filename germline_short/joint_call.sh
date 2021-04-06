#!/bin/bash -e

if [ $# -lt 7 ]
then
    echo usage: $0 [ref_genome] [output.vcf.gz] [dbsnp_vcf] [db_space] [largeTmpDir] [interval] [seqtype]
    exit 1
fi



if [ "$7" = "WGS" ]; then
    interval= 
fi

# contamination data
# max_alternate_alleles, variant_index_parameter, variant_index_type ===> x

# "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx80G"

# --only-output-calls-starting-in-intervals
# Restrict variant output to sites that start within provided intervals. This option can only be activated if intervals are specified.

source activate gatk4
gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" GenotypeGVCFs  \
    -R $1 \
    -O $2 \
    -D $3 \
    --only-output-calls-starting-in-intervals \
    -V gendb://$4 \
    --tmp-dir $5 \
    -L $6
conda deactivate

