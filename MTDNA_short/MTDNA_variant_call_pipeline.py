import subprocess as sp
import os
import glob
import natsort
from jun_tools import jun_mtd as jm  # pip install YjmTool




# qsubManager가 path들 동원해서 이거 실행. 공통 파라미터는 config 파일 읽고 가져오고, 개별 파라미터는 받아와야함 



class MTDNAPipeline:
    
    def __init__(self, _input_dir) -> None:
        
        
        # print(self.input_maf_lst)
        
    
    def run_pipeline(self):
        pass
    
    
    def printReads(self):
        sp.call()
    
    
    






if __name__ == '__main__':
    
    input_dir = r'/data/stemcell/WES/GRCh38/mtDNAcall_test'
    
    input_maf_lst = jm.get_input_path_list(input_dir, '*.bam', False)
    output_dir = jm.set_output_dir(input_dir, 'MTDNA_varinat')
    
    # for루프로 객체 실행 
    
    sp.call()

    test_obj = MTDNAPipeline(input_dir)