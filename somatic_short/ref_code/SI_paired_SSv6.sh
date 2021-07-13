#!/bin/bash -e
if [ $# -lt 2 ]
then
        echo usage: $0 [Tumor bam] [Normal bam]
        exit 1
fi

### variables
config_file=/data/D161740/src/mapping_SSv6_b37.cfg

ref=`grep -w "ref=" $config_file | sed "s/ref=//g"`
java_path=`grep -w "java_path=" $config_file | sed "s/java_path=//g"`
gatk_path=`grep -w "gatk_path=" $config_file | sed "s/gatk_path=//g"`
target_interval=/data/D161740/Reference/Target_intervals/SureSelect/V6/sureselect_v6.interval_list


bam1=$1
bam2=$2
output=`echo $bam1|cut -d"." -f1`

$java_path/java\
	-Xmx4G\
	-jar $gatk_path/GenomeAnalysisTK.jar\
	-T SomaticIndelDetector\
	-R $ref\
	-I:normal $bam2\
	-I:tumor $bam1\
	-o ${output}.somaticindelocator.vcf\
	-L $target_interval\
	--window_size 500\
	-filter T_COV\<2\|\|N_COV\<0\|\|T_INDEL_F\<0.05\|\|T_INDEL_CF\<0.1

01_somaticindel_filter.py -i ${output}.somaticindelocator.vcf

