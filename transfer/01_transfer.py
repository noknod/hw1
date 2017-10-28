#!/usr/bin/env python

import os


ALL_FILES_FILE = '../count/data/m1_files_done.txt'

DONE_FILES_FILE = './data/m1_files_done.txt'


def read_dirs_file(file_path):
    answer = []
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            line = line.strip()
            if len(line) != 0:
                answer.append(line.strip())
    return set(answer)


def main():
    all_files = sored(list(read_dirs_file(ALL_FILES_FILE)))
    done_files = read_dirs_file(DONE_FILES_FILE)
    print 'All {0}, done {1} files'.format(len(all_files), len(done_files))

    for file_path in all_files:
        if file_path not in done_files:
            print(file_path)
            file_date = file_path.split('/')[-2]
            command = 'hdfs dfs -get hw1/metrcics/{0} ./hw1/metrics/{0}/m1_1_2.txt'.format(file_date)
            result_command = int(os.system(command))
            if result_command != 0:
                print '\n\n++++++++++\n\nERROR\n\n++++++++++\n\n'
                break
            add_dir_to_file(file_path, DONE_FILES_FILE)
        break


if __name__ == '__main__':
    main()
