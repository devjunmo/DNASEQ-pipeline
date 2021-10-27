#!/bin/bash -e


if [ $# -lt 7 ]
then
        echo usage: $0 [Tumor bam path] [Germline src] [Ref genome] [interval] [Output prefix] [PON] [seqType]
        exit 1
fi



tumor=$1
germ=$2
ref=$3
target_interval=$4
output_prefix=$5
PON=$6
seqType=$7



source activate gatk4

case "$seqType" in

    "WES")
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" Mutect2 \
            --germline-resource "$germ"\
            -R "$ref"\
            --intervals "$target_interval"\
            -I "$tumor"\
            -O "${output_prefix}"_mutect2.vcf\
            --f1r2-tar-gz "${output_prefix}".f1r2.tar.gz\
            --genotype-germline-sites true\
            -bamout "${output_prefix}"_bamout.bam\
            --panel-of-normals "$PON"
    ;;
    "WGS")
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" Mutect2 \
            --germline-resource "$germ"\
            -R "$ref"\
            -I "$tumor"\
            -O "${output_prefix}"_mutect2.vcf\
            --f1r2-tar-gz "${output_prefix}".f1r2.tar.gz\
            --genotype-germline-sites true\
            --panel-of-normals "$PON"
    ;;
    *)
        echo "seqType = WES or WGS"
        exit 1
    ;;
esac

conda deactivate