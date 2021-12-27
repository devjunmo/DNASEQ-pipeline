#!/bin/bash -e



classpath="${SV_DIR}/lib/SVToolkit.jar:${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar:${SV_DIR}/lib/gatk/Queue.jar"

project_name='pp_inc_genmap'
queue_name='test2'
log_directory='/data_244/stemcell/WES/hg38_gdc/hg38_gdc_all_bam/CNV/Genome_strip/pp_inc_gendermap/test_log'
workflow_manager_options='-R rusage[mem=8192]'

java -Xmx4g -cp ${classpath} \
    org.broadinstitute.gatk.queue.QCommandLine \
    -S ${SV_DIR}/qscript/SVQScript.q
    -S pipeline_script_to_run.q \
    -cp ${classpath} \
    -gatk ${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar \
    -jobProject ${project_name} \
    -jobQueue ${queue_name} \
    -jobLogDir ${log_directory} \
    -jobNative ${workflow_manager_options} \
    -run