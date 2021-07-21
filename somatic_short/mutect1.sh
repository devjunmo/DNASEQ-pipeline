#!/bin/bash -e

if [ $# -lt 12 ]
then
        echo usage: $0 [Tumor bam path] [Normal bam path] [Ref genome] [interval] [PON] [Out txt] [Out vcf] [dbsnp] [cosmic] [seq Type] [java7 path] [mutect path] 
        exit 1
fi


tumor=$1
normal=$2
ref=$3
target_interval=$4
PON=$5
outTxt=$6
outVcf=$7
dbsnp=$8
cosmic=$9
seqType=${10}
java7_path=${11}
mutect_path=${12}



source activate gatk4

case "$seqType" in
    "WES")
        #	--cosmic $cosmic\
        $java7_path\
            -jar\
            -Xmx4G\
            -Djava.io.tmpdir=/data_244/scratch\
            $mutect_path\
            --analysis_type MuTect\
            --reference_sequence $ref\
            --dbsnp $dbsnp\
            --intervals $target_interval\
            --input_file:tumor $tumor\
            --input_file:normal $normal\
            --out $outTxt\
            --vcf $outVcf\
            --normal_panel $PON\
            --enable_extended_output\
            --max_alt_alleles_in_normal_count 5
    ;;
    "WGS")
        #	--cosmic $cosmic\
        $java7_path\
            -jar\
            -Xmx4G\
            -Djava.io.tmpdir=/data_244/scratch\
            $mutect_path\
            --analysis_type MuTect\
            --reference_sequence $ref\
            --dbsnp $dbsnp\
            --input_file:tumor $tumor\
            --input_file:normal $normal\
            --out $outTxt\
            --vcf $outVcf\
            --normal_panel $PON\
            --enable_extended_output\
            --max_alt_alleles_in_normal_count 5
    ;;
    *)
        echo "seqType = WES or WGS"
        exit 1
    ;;
esac

conda deactivate



# grep -v REJECT ${output}.mutect.txt > ${output}.mutect.filtered.txt
# grep -v REJECT ${output}.mutect.vcf > ${output}.mutect.filtered.vcf