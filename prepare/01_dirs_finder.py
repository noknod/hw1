#!/usr/bin/env python

import os
import sys
import re


DONE_DIRS_FILE = './data/done_dirs.txt'


def read_done_dirs(file_path):
    answer = []
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            answer.append(line.strip())
    return answer




def main():
    done_dirs = read_done_dirs(DONE_DIRS_FILE)
    print(done_dirs)
    """files = []
    with open('./dirs.txt', 'r') as infile:
        cnt = 1
        for line in infile.readlines():
            if cnt == 1:
                cnt = 2
            else:
                #print line.strip().split(' ')
                path = line.split(' ')[-1].strip()
                print path
                os.system('hdfs dfs -ls ' + path + ' > ./tmp.txt')
                tmp_cnt = 1
                with open('./tmp.txt', 'r') as tif:
                    for tmp_line in tif.readlines():
                        if tmp_cnt == 1:
                           tmp_cnt = 2
                        else:
                            file_path = tmp_line.split(' ')[-1].strip()
                            print file_path
                            files.append(file_path) 
                #break
    with open ('./files.txt', 'w' ) as outfile:
        for file_path in files:
            outfile.write(file_path + '\n')
    """


if __name__ == '__main__':
    main()

