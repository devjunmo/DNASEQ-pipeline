#!/bin/bash -e

if [ $# -lt 5 ]
then
    echo usage: $0 [INPUT_BAM_FILE] [/path/output.table] [RefGenome] [RAM] [seqType] [interval]
    exit 1
fi


input=$1
output=$2
ref_genome=$3
ram="-Xmx"$4"G"
interval=$6

###### 알려진 변이 site 넣는곳.. 이부분 사용하면서 수정해줘야 함 #######

r_path=/home/jun9485/data/refGenome/b37/

ks_dbSNP=$r_path"dbsnp_138.b37.vcf"
ks_mills=$r_path"Mills_and_1000G_gold_standard.indels.b37.vcf"
ks_1000G=$r_path"1000G_phase1.indels.b37.vcf"

####################################################################

case "$5" in
    "WES")
        source activate gatk4
        gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" BaseRecalibrator \
            -I $input \
            -O $output \
            --known-sites $ks_dbSNP \
            --known-sites $ks_mills \
            --known-sites $ks_1000G \
            -R $ref_genome \
            --use-original-qualities \
            -L $interval
        conda deactivate
    ;;
    "WGS")
        echo "WGS code"
    ;;
    *)
        echo "seqType = WES or WGS"
        exit 1
    ;;
esac

