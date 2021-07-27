import subprocess as sp


input_ref_genome = r'/data_244/refGenome/b37/human_g1k_v37.fasta'

output_path = r'/data_244/utuc/sequenza/b37.gc50Base.wig.gz'


sp.call(rf'sequenza-utils gc_wiggle -w 50 --fasta {input_ref_genome} -o {output_path}', shell=True)