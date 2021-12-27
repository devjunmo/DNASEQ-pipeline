#!/bin/bash -e

if [ $# -lt 8 ]
then
    echo usage: $0 [INPUT_VCF] [/path/outputPrefix] [RefGenome] [RefGenomeDir] [seqType] [interval] [refVer] [varType]
    exit 1
fi


inputVCF=$1
output_prefix=$2
ref_genome=$3
ref_dir=$4
seqType=$5
interval=$6
refVer=$7
varType=$8


case "$refVer" in
    "b37")
        snp_ks='path'
    ;;

    "hg38")
        snp_ks_hapmap=$ref_dir"/hapmap_3.3.hg38.vcf.gz"
        snp_ks_omni=$ref_dir"/1000G_omni2.5.hg38.vcf.gz"
        snp_ks_1KGP1=$ref_dir"/1000G_phase1.snps.high_confidence.hg38.vcf.gz"
        snp_ks_dbsnp=$ref_dir"/Homo_sapiens_assembly38.dbsnp138.vcf.gz"
    ;;

    *)
        echo "refVer = b37 or hg38"
    ;;
esac



source activate gatk4

case "$varType" in
    SNP)
        case "$seqType" in
            WGS)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" VariantRecalibrator \
                    -R ${ref_genome} \
                    -V ${inputVCF} \
                    --resource:hapmap,known=false,training=true,truth=true,prior=15.0 ${snp_ks_hapmap} \
                    --resource:omni,known=false,training=true,truth=false,prior=12.0 ${snp_ks_omni} \
                    --resource:1000G,known=false,training=true,truth=false,prior=10.0 ${snp_ks_1KGP1} \
                    --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 ${snp_ks_dbsnp} \
                    -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
                    -mode ${varType} \
                    -O ${output_prefix}.recal \
                    --tranches-file ${output_prefix}.tranches \
                    --rscript-file ${output_prefix}.plots.R
            ;;
            WES)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" VariantRecalibrator \
                    -R ${ref_genome} \
                    -V ${inputVCF} \
                    --resource:hapmap,known=false,training=true,truth=true,prior=15.0 ${snp_ks_hapmap} \
                    --resource:omni,known=false,training=true,truth=false,prior=12.0 ${snp_ks_omni} \
                    --resource:1000G,known=false,training=true,truth=false,prior=10.0 ${snp_ks_1KGP1} \
                    --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 ${snp_ks_dbsnp} \
                    -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
                    -mode ${varType} \
                    -O ${output_prefix}.recal \
                    --tranches-file ${output_prefix}.tranches \
                    --rscript-file ${output_prefix}.plots.R \
                    -L ${interval}
            ;;
            *)
                echo "WGS, WES check"
                exit 1
            ;;
        esac

    ;;
    INDEL)
        case "$seqType" in
            WGS)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms30G -Xmx30G" VariantFiltration \
                    -V $input_vcf \
                    -filter "QD < 2.0" --filter-name "QD2" \
                    -filter "QUAL < 30.0" --filter-name "QUAL30" \
                    -filter "FS > 200.0" --filter-name "FS200" \
                    -filter "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20" \
                    -O $output_vcf
            ;;
            WES)
                gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" VariantFiltration \
                    -V $input_vcf \
                    --filter "QD < 2.0" --filter-name "QD2" \
                    -filter "QUAL < 30.0" --filter-name "QUAL30" \
                    -filter "FS > 200.0" --filter-name "FS200" \
                    -filter "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20" \
                    -L $interval \
                    -O $output_vcf
            ;;
            *)
                echo "WGS, WES check"
                exit 1
            ;;
        esac
    ;;
    *)
        echo "SNP, INDEL check"
        exit 1
    ;;
esac

# conda deactivate
