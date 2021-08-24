#!/bin/bash -e

if [ $# -lt 6 ]
then
    echo usage: $0 [fastq1] [fastq2] [~/path/outputName.sam] [threads] [RefGenome] [readName]
    exit 1
fi


fastq1=$1
fastq2=$2
output_path=$3
threads=$4
ref_genome=$5
readName=$6

# 같은샘플 다른배치 merge할때 바코딩 목적  Read Group
RG="@RG\tID:$readName\tPL:illumina\tPU:ex\tLB:$readName\tSM:$readName" # 이 부분 피드백


# -T: minimum score to output 디폴트 30, 저번 RNA데이터 기준 필터 30 이하는 전체의 10%정도
# -M: Mark shorter split hits as secondary (for Picard compatibility). -> picard 안쓸건데 해야하는지
# -w band width params. gaps longer than INT will not be found. 기본값 100

source activate gatk4
bwa mem \
    -t $threads\
    -T 0\
    -R $RG\
    $ref_genome $fastq1 $fastq2 > $output_path
    
conda deactivate

sleep 10s