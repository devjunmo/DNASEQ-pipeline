#!/bin/bash -e

if [ $# -lt 5 ]
then
    echo usage: $0 [input.vcf] [RefGenome] [refVersion] [1D/2D] [seqType]
    exit 1
fi



case "$4" in
    1D)
        key="pass"
    ;;
    2D)
        key="CNN_2D"
    ;;
    *)
        echo "1D, 2D를 설정하시오"
        exit 1
    ;;
esac




gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" Funcotator \
     --variant variants.vcf \
     --reference Homo_sapiens_assembly19.fasta \
     --ref-version hg19 \
     --data-sources-path funcotator_dataSources.v1.2.20180329 \
     --output variants.funcotated.maf \
     --output-file-format MAF