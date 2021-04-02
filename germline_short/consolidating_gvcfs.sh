#!/bin/bash -e

if [ $# -lt 7 ]
then
    echo usage: $0 [dbDir] [batchSize] [interval] [mapfile] [tmpdir] [thread] [seqtype]
    exit 1
fi



if [ "$7" = "WGS" ]; then
    interval= 
fi

# contamination data
# max_alternate_alleles, variant_index_parameter, variant_index_type ===> x

# "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xmx80G"
source activate gatk4
gatk --java-options "-Xmx80G" GenomicsDBImport \
    --genomicsdb-workspace-path $1 \
    --batch-size $2 \
    -L $3 \
    --sample-name-map $4 \
    --tmp-dir $5 \
    --reader-threads $6 \
conda deactivate

