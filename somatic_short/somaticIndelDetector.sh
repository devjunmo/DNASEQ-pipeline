#!/bin/bash -e

if [ $# -lt 11 ]
then
        echo usage: $0 [Tumor bam path] [Normal bam path] [Ref genome] [interval] [PON] [Out vcf] [dbsnp] [cosmic] [seq Type] [java7 path] [gatk path] 
        exit 1
fi


tumor=$1
normal=$2
ref=$3
target_interval=$4
PON=$5

outVcf=$6
dbsnp=$7
cosmic=$8
seqType=$9
java7_path=${10}
gatk_path=${11}



source activate gatk4

case "$seqType" in
    "WES")
        $java7_path\
            -jar\
            -Xmx4G\
            -Djava.io.tmpdir=/data_244/scratch\
            $gatk_path\
            -T SomaticIndelDetector\
            -R $ref\
            -L $target_interval\
            -I:tumor $tumor\
            -I:normal $normal\
            -o $outVcf\
            --window_size 500\
            -filter T_COV\<2\|\|N_COV\<0\|\|T_INDEL_F\<0.05\|\|T_INDEL_CF\<0.1
    ;;
    "WGS")
        $java7_path\
            -jar\
            -Xmx4G\
            -Djava.io.tmpdir=/data_244/scratch\
            $gatk_path\
            -T SomaticIndelDetector\
            -R $ref\
            -I:tumor $tumor\
            -I:normal $normal\
            -o $outVcf\
            --window_size 500\
            -filter T_COV\<2\|\|N_COV\<0\|\|T_INDEL_F\<0.05\|\|T_INDEL_CF\<0.1
    ;;
    *)
        echo "seqType = WES or WGS"
        exit 1
    ;;
esac

conda deactivate


# 01_somaticindel_filter.py -i ${output}.somaticindelocator.vcf