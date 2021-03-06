#!/usr/bin/env python

import os
import sys
import re


ALL_DIRS_FILE = './data/all_dirs.txt'

DONE_DIRS_FILE = './data/done_dirs.txt'

HADOOP_LOGS_DIR = '/user/bigdatashad/logs/'

HADOOP_HW1_METRICS_PATH = 'hw1/metrics/{0}'


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
        if current_dir != 'items':
            dirs.append(current_dir)
    return dirs


def add_dir_to_file(current_dir, file_path):
    with open(file_path, 'a') as outfile:
        outfile.write(current_dir)
        outfile.write('\n')


def find_new_dirs(hadoop_logs_dir, all_dirs_file_path, done_dirs_file_path):
    new_dirs = []
    all_dirs = read_dirs_file(all_dirs_file_path)
    done_dirs = read_dirs_file(done_dirs_file_path)

    dir_list = find_all_dirs(HADOOP_LOGS_DIR)
    for current_dir in dir_list:
        if current_dir not in all_dirs:
            print 'Add new dir {0}'.format(current_dir)
            add_dir_to_file(current_dir, ALL_DIRS_FILE)
            new_dirs.append(current_dir)
    return new_dirs


def create_dir_in_hadoop(hadoop_dir_path):
    command = 'hdfs dfs -mkdir {0}'.format(hadoop_dir_path)
    result_command = int(os.system(command))
    if result_command != 0:
        print '\n\n---------\n\nERROR\n\n---------\n\n'
        return False
    return True


def check_hadoop_dir_exist(hadoop_path):
    #print 'check', hadoop_path
    command = 'hdfs dfs -test -d {0} && echo "yes" || echo "no"'.format(hadoop_path)
    stream = os.popen(command)
    #result = stream.readlines()
    #print(result)
    return (stream.readlines()[0].strip() == 'yes')
    #return True


def main():
    all_dirs = read_dirs_file(ALL_DIRS_FILE)
    done_dirs = read_dirs_file(DONE_DIRS_FILE)
    print 'All {0}, done {1} dirs'.format(len(all_dirs), len(done_dirs))
    
    new_dirs = find_new_dirs(HADOOP_LOGS_DIR, ALL_DIRS_FILE, DONE_DIRS_FILE)
    print '\nFound {0} new dirs\n'.format(len(new_dirs))
    
    cnt = 0
    #for current_dir in all_dirs:
    #for current_dir in ['/user/bigdatashad/logs/2017-10-28']:#new_dirs:
    for current_dir in new_dirs:
        dir_date = current_dir.split('/')[-1]
        print dir_date
        hadoop_dir_path = HADOOP_HW1_METRICS_PATH.format(dir_date)
        #print 'hadoop_dir_path', hadoop_dir_path

        is_exists_path = check_hadoop_dir_exist(hadoop_dir_path)        
        if not is_exists_path:
            print  'Need to create {0}'.format(hadoop_dir_path)
            if not create_dir_in_hadoop(hadoop_dir_path):
                break
            cnt += 1

        add_dir_to_file(current_dir, DONE_DIRS_FILE)
        print ''
        #break

    print 'Created neccessary dirs in Hadoop for {0}, {1} was created before'.format(cnt, len(new_dirs) - cnt)


if __name__ == '__main__':
    main()

