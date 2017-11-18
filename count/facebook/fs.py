#!/usr/bin/env python


import os
import sys

from datetime import datetime
from datetime import timedelta


TEMPLATE = """
#!/usr/bin/env bash

OUT_DIR=out
NUM_REDUCERS=1 # > 0 to run the Reduce phase
CONFIG="--config /home/agorokhov/conf.empty"

hdfs dfs -rm -r -skipTrash out

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="Uniq users dates" \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -D mapreduce.job.maps=50 \
    -files fs_mapper.py,fs_reducer.py,dates_users.dat \
    -mapper "./fs_mapper.py" \
    -reducer "./fs_reducer.py" \
    -input {0} \
    -output out
"""


ALL_FILES_FILE = '../../prepare/data/all_files.txt'

DONE_FILES_FILE = '../data/fs_files_done.txt'

START_DATE = datetime.strptime('2017-09-01', '%Y-%m-%d').date()


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

    #file_path = '/user/yuklyushkin/hw1/metrics/2017-10-01/users.txt'
    #command = TEMPLATE.format(file_path, '/user/yuklyushkin/hw1/users_date.txt')
    #result_code = int(os.system(command))
    #if result_code != 0:
    #        print '\n\n*********\n\nERROR\n\n*********\n\n'
    #print '\ncomputed\n'

    #"""
    cnt = 0
    for file_path in all_files:
        if file_path not in done_files:

            #if file_path.split('/')[-2] > '2017-09-05':
            if file_path.split('/')[-2] < '2017-11-13':
                #break
                continue

            print(file_path)
            str_date_file = file_path.split('/')[-2]

            date_file = datetime.strptime(str_date_file, '%Y-%m-%d').date()
            begin_date = date_file + timedelta(days=-2)
            if begin_date < START_DATE:
                begin_date = START_DATE 
            print(date_file, begin_date)

            previous_file_dates = []
            for n in range(int((date_file - begin_date).days)):
                dummy = begin_date + timedelta(n)
                previous_file_dates.append(
                    'hdfs:///user/yuklyushkin/hw1/metrics/{0}/new_facebook_users.txt'.format(dummy))
                previous_file_dates.append(
                    'hdfs:///user/yuklyushkin/hw1/metrics/{0}/signup.txt'.format(dummy))
            prevfiles = ','.join(previous_file_dates)
            #print(prevfiles)

            with open('./dates_users.dat', 'w') as outfile:
                outfile.write(str_date_file)

            #date_file_path = '/user/bigdatashad/logs/{0}/access.log.{1}'.format(str_date_file, str_date_file)
            #if len(prevfiles) != 0:
            #    prevfiles = ',' + prevfiles
            #command = TEMPLATE.format(date_file_path, prevfiles)
            command = TEMPLATE.format(prevfiles)
            #print(command)
            result_code = int(os.system(command))
            if result_code != 0:
                print '\n\n*********\n\nERROR\n\n*********\n\n'
                break
            print '\ncomputed\n'

            dir_path = file_path.split('/')[-2]
            command = 'hdfs dfs -cp out/part-00000 hw1/metrics/{0}/fs.txt'.format(dir_path)
            result_command = int(os.system(command))
            if result_command != 0:
                print '\n\n++++++++++\n\nERROR\n\n++++++++++\n\n'
                break
            add_dir_to_file(file_path, DONE_FILES_FILE)
       
        #cnt += 1
        #if cnt == 4:     
        #    break
        #break
    #"""


if __name__ == '__main__':
    main()
