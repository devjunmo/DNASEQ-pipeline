 #!/bin/bash -e

 
classpath="${SV_DIR}/lib/SVToolkit.jar:${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar:${SV_DIR}/lib/gatk/Queue.jar"
 

ref_genome='/data_244/refGenome/hg38/GDC/GRCh38.d1.vd1.fa'
input_lst='/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/CNV/Genome_strip/pp_v3/stem_all_bam.list'
out_meta_dir='/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/CNV/Genome_strip/pp_v3/meta_data'
pp_log_dir='/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/CNV/Genome_strip/pp_v3/log_pp'

meta_dir='/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/CNV/Genome_strip/pp_v3/meta_data'
gender_mask='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.gendermask.bed'
ploid_map='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.ploidymap.txt'
sv_mask='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.svmask.fasta'
rd_mask='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.rdmask.bed'
gc_mask='/data_244/FTP_DOWN/Homo_sapiens_assembly38/Homo_sapiens_assembly38.gcmask.fasta'
interval_path='/data_244/refGenome/hg38/v0/interval_file/split_interval/whole/S07604514_Padded_onlypos_interval.list'
run_dir='/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/CNV/Genome_strip/pp_v3/CNV_run1'


java -Xmx50g -cp ${classpath} \
     org.broadinstitute.gatk.queue.QCommandLine \
     -S ${SV_DIR}/qscript/discovery/cnv/CNVDiscoveryPipeline.q \
     -S ${SV_DIR}/qscript/SVQScript.q \
     -cp ${classpath} \
     -gatk ${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar \
     -configFile ${SV_DIR}/conf/genstrip_parameters.txt \
     -R ${ref_genome} \
     -I ${input_lst} \
     -md ${meta_dir} \
     -runDirectory ${run_dir} \
     -jobLogDir ${run_dir}/logs \
     -intervalList ${interval_path} \
     -tilingWindowSize 1000 \
     -tilingWindowOverlap 500 \
     -maximumReferenceGapLength 1000 \
     -boundaryPrecision 100 \
     -minimumRefinedLength 500 \
     -run