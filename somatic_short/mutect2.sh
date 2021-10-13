#!/bin/bash -e


if [ $# -lt 9 ]
then
        echo usage: $0 [Tumor bam path] [Normal bam path] [Normal name] [Germline src] [Ref genome] [interval] [Output prefix] [PON] [seqType]
        exit 1
fi



tumor=$1
normal=$2
nname=$3
germ=$4
ref=$5
target_interval=$6
output_prefix=$7
PON=$8
seqType=$9



source activate gatk4

case "$seqType" in
    "WES")
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" Mutect2 \
            --germline-resource "$germ"\
            -R "$ref"\
            --intervals "$target_interval"\
            -I "$tumor"\
            -I "$normal"\
            -normal "$nname"\
            -O "${output_prefix}"_mutect2.vcf\
            --f1r2-tar-gz "${output_prefix}".f1r2.tar.gz\
            -bamout "${output_prefix}"_bamout.bam\
            --panel-of-normals "$PON"
    ;;
    "WGS")
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" Mutect2 \
            --germline-resource "$germ"\
            -R "$ref"\
            -I "$tumor"\
            -I "$normal"\
            -normal "$nname"\
            -O "${output_prefix}"_mutect2.vcf\
            --f1r2-tar-gz "${output_prefix}".f1r2.tar.gz\
            --panel-of-normals "$PON"
    ;;
    *)
        echo "seqType = WES or WGS"
        exit 1
    ;;
esac

conda deactivate