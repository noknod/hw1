#!/usr/bin/env python

import os
import sys
import re


ALL_FILES_FILE = '../hw1/hw1/prepare/data/all_files.txt'

DONE_DIRS_FILE = './data/done_dirs.txt'

DONE_FILES_FILE = './data/done_files.txt'


def read_dirs_file(file_path):
    answer = []
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            line = line.strip()
            if len(line) != 0:
                answer.append(line.strip())
    return set(answer)


def check_hadoop_dir_exists(hadoop_path):
    command = 'hdfs dfs -test -d {0} && echo "yes" || echo "no"'.format(hadoop_path)
    stream = os.popen(command)
    return (stream.readlines()[0].strip() == 'yes')


def find_all_files(hadoop_logs_dir):
    if not check_hadoop_dir_exists(hadoop_logs_dir):
        return None
    files = []
    command = 'hdfs dfs -ls {0}'.format(hadoop_logs_dir)
    stream = os.popen(command)
    for line in stream.readlines():
        line = line.strip()
        pos = line.rfind(' ')
        #print pos
        current_file = line[pos:].strip()
        #print current_dir
        if current_file != 'items':
            files.append(current_file)
    return files


def add_dir_to_file(current_dir, file_path):
    with open(file_path, 'a') as outfile:
        outfile.write(current_dir)
        outfile.write('\n')


def find_new_files(hadoop_logs_dir, all_files_file_path, done_files_file_path):
    new_files = []
    all_files = read_dirs_file(all_files_file_path)
    done_files = read_dirs_file(done_files_file_path)

    file_list = find_all_files(hadoop_logs_dir)
    if file_list is None:
        print 'Not exists now'

    else:
        for current_file in file_list:
            if current_file not in all_files:
                print 'Add new file {0}'.format(current_file)
                add_dir_to_file(current_file, ALL_FILES_FILE)
                new_files.append(current_file)
            add_dir_to_file(hadoop_logs_dir, DONE_FILES_FILE)
    return new_files


def main():
    all_files = read_dirs_file(ALL_FILES_FILE)
    done_dirs = sorted(list(read_dirs_file(DONE_DIRS_FILE)))
    #sorted(done_dirs)
    done_files = read_dirs_file(DONE_FILES_FILE)
    print 'All dirs {0}, done {1} files'.format(len(done_dirs), len(done_files))

    cnt = 0
    for hadoop_logs_dir in done_dirs:
        if hadoop_logs_dir not in done_files:
	    print hadoop_logs_dir
            new_files = find_new_files(hadoop_logs_dir, ALL_FILES_FILE, DONE_FILES_FILE)
            print 'Found {0} new files\n'.format(len(new_files))
            cnt += len(new_files)
    
        #break
    print 'Found total {0} new files'.format(cnt)

if __name__ == '__main__':
    main()

