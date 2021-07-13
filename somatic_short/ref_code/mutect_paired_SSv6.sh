#!/bin/bash -e
if [ $# -lt 2 ]
then
        echo usage: $0 [Tumor bam] [Normal bam]
        exit 1
fi

### variables
config_file=/data/D161740/src/mapping.cfg

ref=`grep -w "ref=" $config_file | sed "s/ref=//g"`
java7_path=`grep -w "java7_path=" $config_file | sed "s/java7_path=//g"`
gatk_path=`grep -w "gatk_path=" $config_file | sed "s/gatk_path=//g"`
mutect_path=`grep -w "mutect_path=" $config_file | sed "s/mutect_path=//g"`
dbsnp_common=`grep -w "dbsnp_common=" $config_file | sed "s/dbsnp_common=//g"`
dbsnp=`grep -w "dbsnp=" $config_file | sed "s/dbsnp=//g"`
cosmic=`grep -w "cosmic=" $config_file | sed "s/cosmic=//g"`
target_interval=/data/D161740/Reference/Target_intervals/SureSelect/V6/sureselect_v6.interval_list
PON=`grep -w "PON=" $config_file | sed "s/PON=//g"`

echo $target_interval

bam1=$1
bam2=$2
output=`echo $bam1|cut -d"." -f1`

#	--cosmic $cosmic\
#	--intervals $target_interval\
$java7_path/java\
	-jar\
	-Xmx4G\
	-Djava.io.tmpdir=/data/scratch\
	$mutect_path/mutect-1.1.7.jar\
	--analysis_type MuTect\
	--reference_sequence $ref\
	--dbsnp $dbsnp\
	--intervals $target_interval\
	--input_file:tumor $bam1\
	--input_file:normal $bam2\
	--out ${output}.mutect.txt\
	--vcf ${output}.mutect.vcf\
	--normal_panel $PON\
	--enable_extended_output\
	--max_alt_alleles_in_normal_count 5

grep -v REJECT ${output}.mutect.txt > ${output}.mutect.filtered.txt
grep -v REJECT ${output}.mutect.vcf > ${output}.mutect.filtered.vcf
