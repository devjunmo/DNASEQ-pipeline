import subprocess as sp


# input_ref_genome = r'/data_244/refGenome/b37/human_g1k_v37.fasta'
input_ref_genome = r'/data_244/refGenome/hg38/GDC/GRCh38.d1.vd1.fa'

# output_path = r'/data_244/utuc/sequenza/b37.gc50Base.wig.gz'
output_path = r'/data_244/utuc/utuc_gdc/CNV/sequenza/hg38_gdc.gc50Base.wig.gz'


sp.call(rf'sequenza-utils gc_wiggle -w 50 --fasta {input_ref_genome} -o {output_path}', shell=True)