import subprocess as sp
import glob
# import natsort
import time
import sys
import getopt
import os

test = ''

def main(argv):
    file_name = argv[0]
    global test

    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:", ["help", "test="])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(file_name, 'option error')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        print(opt)
        if opt in ("-h", "--help"):  # HELP 요청인 경우 사용법 출력
            print(file_name, 'file name..')
            sys.exit(0)
        elif opt in ("-t", "--test"):
            test = arg

main(sys.argv)

print(test)
