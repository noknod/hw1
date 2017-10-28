#!/usr/bin/env python

import os
import sys
import re


ALL_DIRS_FILE = './data/all_dirs.txt'

DONE_DIRS_FILE = './data/done_dirs.txt'


def read_dirs_file(file_path):
    answer = []
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            line = line.strip()
            if len(line) != 0:
                answer.append(line.strip())
    return set(answer)


def create_dir_local(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return True
    return False


def main():
    done_dirs = read_dirs_file(DONE_DIRS_FILE)
    print 'Done {0} dirs'.format(len(done_dirs))
    
    cnt = 0
    for current_dir in done_dirs:
        dir_date = current_dir.split('/')[-1]
        print dir_date
        dir_path = 'metrics/{0}'.format(dir_date)
        #print 'dir_path', dir_path

        if create_dir_local(dir_path):
            print  'Created {0}'.format(dir_path)
            cnt += 1

        print ''
        #break

    print 'Created local dirs for {0}, {1} was created before'.format(cnt, len(done_dirs) - cnt)


if __name__ == '__main__':
    main()

