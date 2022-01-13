#!/bin/bash -e


classpath="${SV_DIR}/lib/SVToolkit.jar:${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar:${SV_DIR}/lib/gatk/Queue.jar"

project_name='testPrj'
queue_name='testQ'
log_directory='/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/CNV/Genome_strip/test'
workflow_manager_options='-R rusage[mem=8192]'

# ref_genome='/data_244/refGenome/hg38/v0/gdc/GRCh38.d1.vd1.fa'
ref_genome='/data_244/refGenome/hg38/v0/Homo_sapiens_assembly38.fasta'

input_lst='/data_244/stemcell/WES/hg38_gatk/teratoma/CNV/STRiP/test/stem_gatk_bam_test.list'
out_meta_dir='/data_244/stemcell/WES/hg38_gatk/teratoma/CNV/STRiP/test/meta_data'
pp_log_dir='/data_244/stemcell/WES/hg38_gatk/teratoma/CNV/STRiP/test/log_pp'

gender_mask='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.gendermask.bed'
ploid_map='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.ploidymap.txt'
sv_mask='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.svmask.fasta'
rd_mask='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.rdmask.bed'
gc_mask='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.gcmask.fasta'


java -Xmx50g -cp ${classpath} \
    org.broadinstitute.gatk.queue.QCommandLine \
    -S ${SV_DIR}/qscript/SVPreprocess.q \
    -S ${SV_DIR}/qscript/SVQScript.q \
    -cp ${classpath} \
    -gatk ${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar \
    -configFile ${SV_DIR}/conf/genstrip_parameters.txt \
    -R ${ref_genome} \
    -I ${input_lst} \
    -md ${out_meta_dir} \
    -bamFilesAreDisjoint true \
    -jobLogDir ${pp_log_dir} \
    -genderMaskBedFile ${gender_mask} \
    -ploidyMapFile ${ploid_map} \
    -genomeMaskFile ${sv_mask} \
    -readDepthMaskFile ${rd_mask} \
    -copyNumberMaskFile ${gc_mask} \
    -run