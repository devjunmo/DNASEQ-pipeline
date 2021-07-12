#!/bin/bash -e
if [ $# -lt 2 ]
then
        echo usage: $0 [Tumor bam] [Normal bam]
        exit 1
fi

### variables
config_file=/data/D161740/src/mapping_OPAMCv4.3s.cfg

ref=/data/D161740//Reference/Human/b37/human_g1k_v37.fa
#target_interval=/data/D161740/Research/Cancer/On-going/ks2/WES/fastq/SureSelect_v6.interval_list
#target_interval=/data/D161740/Research/Cancer/On-going/ks2/WES/fastq/SSV6.b37.interval_list
#target_interval=/data/D161740/Reference/Target_intervals/SureSelect/V6/sureselect_v6.interval_list
target_interval='/data/D161740/Reference/Target_intervals/SureSelect/V6_UTR/sureselect_v6UTR.interval_list'
PON=/data/D161740/Reference/PON/mutect2/PON_snv_indel_merged.sorted2.vcf
germ=/data/D161740/Reference/GATK_bundle/2.8/b37/af-only-gnomad.raw.sites.b37.vcf.gz
sec=/data/D161740/Reference/GATK_bundle/GetPileupSummaries/small_exac_common_3_b37.vcf.gz

normal=$2
tumor=$1
output=`echo $tumor|cut -d"." -f1`
nname=`echo $normal|cut -d"." -f1`

source activate ngs2

#	--disable-read-filter MateOnSameContigOrNoMappedMateReadFilter \
#gatk Mutect2\
#	--initial-tumor-lod 2.0\
#	--normal-lod 2.2\
#	--tumor-lod-to-emit 3.0\
#	--pcr-indel-model CONSERVATIVE\
#	--germline-resource $germ\
#	--af-of-alleles-not-in-resource 0 \
#	--genotype-germline-sites true \
#	--force-active true \
#	-R $ref\
#	--intervals $target_interval\
#	-I $bam1\
#	-I $bam2\
#	-normal $nname\
#	-tumor $output\
#	-O ${output}.mutect.vcf\
#	--f1r2-tar-gz ${output}.f1r2.tar.gz\
#	--panel-of-normals $PON

gatk Mutect2\
	--germline-resource $germ\
	-R $ref\
	--intervals $target_interval\
	-I $tumor\
	-I $normal\
	-normal $nname\
	-O ${output}.mutect.vcf\
	--f1r2-tar-gz ${output}.f1r2.tar.gz\
	--panel-of-normals $PON
	
gatk LearnReadOrientationModel\
	-I ${output}.f1r2.tar.gz\
	-O ${output}.rom.tar.gz

gatk GetPileupSummaries \
	-I $tumor \
	-V $sec \
	-L $sec \
	-O ${output}.getpileupsummaries.table

gatk CalculateContamination \
	-I ${output}.getpileupsummaries.table \
	-tumor-segmentation ${output}.segments.table \
	-O ${output}.calculatecontamination.table


gatk FilterMutectCalls\
	-V ${output}.mutect.vcf \
	-R $ref\
	--tumor-segmentation ${output}.segments.table \
	--contamination-table ${output}.calculatecontamination.table \
	--ob-priors ${output}.rom.tar.gz \
	-O ${output}.mutect.filtered.vcf

cat ${output}.mutect.filtered.vcf | grep -v '#' | awk '$7=="PASS"' > ${output}.mutect.filtered.ext.vcf
grep '#' ${output}.mutect.filtered.vcf| cat - ${output}.mutect.filtered.ext.vcf > ${output}.mutect.filtered.final.vcf


source deactivate
