#!/bin/bash -e

if [ $# -lt 3 ]
then
    echo usage: $0 [input_path] [working_dir] [tumor_contents]
    exit 1
fi


input=$1
wd=$2
tc=$3



source activate pyclone

PyClone run_analysis_pipeline \
    --in_files $input\
    --working_dir $wd\
    --tumour_contents $tc    

conda deactivate
