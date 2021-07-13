#!/bin/bash -e


if [ $# -lt 6 ]
then
        echo usage: $0 [input.mutectl.vcf] [output.mutect.filtered.vcf] [ref genome] [i.segment.table] [i.calculatecontamination.table] [i.rom.tar.gz]
        exit 1
fi



input_vcf=$1
output_vcf=$2
ref=$3
seg_table=$4
contam_table=$5
ob_prior=$6


source activate gatk4

gatk FilterMutectCalls\
	-V "$input_vcf" \
	-R "$ref" \
	--tumor-segmentation "$seg_table" \
	--contamination-table "$contam_table" \
	-ob-priors "$ob_prior" \
	-O "$output_vcf"

conda deactivate