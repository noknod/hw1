#!/usr/bin/env python


import os
import sys
import re

# 196.223.28.31 - - [16/Nov/2015:00:00:00 +0400] "GET /photo/manage.cgi HTTP/1.1" 200 0 "-" "Mozilla/6.66"


TEMPLATE = """
#!/usr/bin/env bash

OUT_DIR=out
NUM_REDUCERS=1 # > 0 to run the Reduce phase
CONFIG="--config /home/agorokhov/conf.empty"

hdfs dfs -rm -r -skipTrash out

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="Uniq users step1" \
    -D mapreduce.job.maps=50 \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files metric03_mapper.py,metric03_reducer.py,IP2LOCATION-LITE-DB1.CSV,ipcountry.py \
    -mapper "./metric03_mapper.py" \
    -reducer "./metric03_reducer.py" \
    -input hdfs://{0} \
    -output out
"""


ALL_FILES_FILE = '../prepare/data/all_files.txt'

DONE_FILES_FILE = './data/m3_files_done.txt'


def read_dirs_file(file_path):
    answer = []
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            line = line.strip()
            if len(line) != 0:
                answer.append(line.strip())
    return set(answer)


def add_dir_to_file(current_dir, file_path):
    with open(file_path, 'a') as outfile:
        outfile.write(current_dir)
        outfile.write('\n')


def main():
    all_files = sorted(list(read_dirs_file(ALL_FILES_FILE)))
    done_files = read_dirs_file(DONE_FILES_FILE)
    print 'All {0}, done {1} files'.format(len(all_files), len(done_files))

    for file_path in all_files:
        if file_path not in done_files:
            date_str = file_path.split('/')[-2]
            #if date_str < '2017-10-29':
            #    continue

            print file_path
            saved_file_path = file_path
            file_path = '/user/yuklyushkin/hw1/metrics/{0}/users.txt'.format(date_str)
            command = TEMPLATE.format(file_path)
            #break
            result_code = int(os.system(command))
            if result_code != 0:
                print '\n\n*********\n\nERROR\n\n*********\n\n'
                break
            print '\ncomputed\n'

            dir_path = file_path.split('/')[-2]
            command = 'hdfs dfs -cp out/part-00000 hw1/metrics/{0}/m3.txt'.format(dir_path)
            result_command = int(os.system(command))
            if result_command != 0:
                print '\n\n++++++++++\n\nERROR\n\n++++++++++\n\n'
                break
            add_dir_to_file(saved_file_path, DONE_FILES_FILE)
            
        #break


if __name__ == '__main__':
    main()
