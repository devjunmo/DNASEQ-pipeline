
#!/bin/bash -e

if [ $# -lt 2 ]
then
    echo usage: $0 [input_VCFs] [out.vcf]
    exit 1
fi

inputVCFs=$1
echo $input_VCFs
outVCF=$2

inputArray=()
inputArray+=($input_VCFs)
echo $inputArray

# source activate gatk4

# gatk --java-options "-XX:ParallelGCThreads=1 -XX:ConcGCThreads=1 -Xms20G -Xmx20G" GatherVcfs \
#     -I $inputArray \
#     -O $outVCF

# conda deactivate