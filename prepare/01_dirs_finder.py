#!/usr/bin/env python

import os
import sys
import re


ALL_DIRS_FILE = './data/all_dirs.txt'

DONE_DIRS_FILE = './data/done_dirs.txt'

HADOOP_LOGS_DIR = '/user/bigdatashad/logs/'


def read_dirs_file(file_path):
    answer = []
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            line = line.strip()
            if len(line) != 0:
                answer.append(line.strip())
    return set(answer)



def find_all_dirs(hadoop_logs_dir):
    dirs = []
    command = 'hdfs dfs -ls {0}'.format(hadoop_logs_dir)
    stream = os.popen(command)
    for line in stream.readlines():
        line = line.strip()
        pos = line.rfind(' ')
        #print pos
        current_dir = line[pos:].strip()
        #print current_dir
        dirs.append(current_dir)
    return dirs


def add_dir_to_file(current_dir, file_path):
    with open(file_path, 'a') as outfile:
        outfile.write(current_dir)
        outfile.write('\n')


def main():
    all_dirs = read_dirs_file(ALL_DIRS_FILE)
    done_dirs = read_dirs_file(DONE_DIRS_FILE)
    print 'All {0}, done {1} dirs'.format(len(all_dirs), len(done_dirs))
    
    dir_list = find_all_dirs(HADOOP_LOGS_DIR)
    for current_dir in dir_list:
        if current_dir not in all_dirs:
            print 'Add new dir {0}'.format(current_dir)
            add_dir_to_file(current_dir, ALL_DIRS_FILE)

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

