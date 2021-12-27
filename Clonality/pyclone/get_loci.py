
# Output dir에 있는 table > loci.tsv를 이름바꿔주고, 한군데다가 복사하는 코드

import os

def print_files_in_dir(root_dir, prefix):
    files = os.listdir(root_dir)
    for file in files:
        path = os.path.join(root_dir, file)
        print(prefix + path)

root_dir = "./test/"
print_files_in_dir(root_dir, "")