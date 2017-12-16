#!/usr/bin/env python


import os
import sys

from datetime import datetime, timedelta


TEMPLATE = """
#!/usr/bin/env bash

OUT_DIR=out
NUM_REDUCERS=1 # > 0 to run the Reduce phase
CONFIG="--config /home/agorokhov/conf.empty"

hdfs dfs -rm -r -skipTrash out

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="KUA HW 3 metric 4" \
    -D mapreduce.job.maps=20 \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files m4_mapper.py,m4_reducer.py,m4_date.dat \
    -mapper "./m4_mapper.py" \
    -reducer "./m4_reducer.py" \
    -input {0} \
    -output out
"""

ALL_FILES_FILE = './data/profiles_users_files_done.txt'

DONE_FILES_FILE = './data/m4_files_done.txt'

START_DATE = datetime.strptime('2017-12-06', '%Y-%m-%d').date()


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
            str_date_file = file_path.split('/')[-2]
            if str_date_file < '2017-12-06':
                continue                
            #if str_date_file >= '2017-12-11':
            #    break
            #print(file_path)

            date_file = datetime.strptime(str_date_file, '%Y-%m-%d').date()
            begin_date = date_file + timedelta(days=-4)
            if begin_date < START_DATE:
                begin_date = START_DATE 
            print(date_file, begin_date)

            previous_file_dates = []
            for n in range(int((date_file - begin_date).days) + 1):
                dummy = begin_date + timedelta(n)
                previous_file_dates.append(
                    'hdfs:///user/yuklyushkin/hw1/metrics/{0}/profiles_users.txt'.format(dummy))
            prevfiles = ','.join(previous_file_dates)
            print(prevfiles)

            with open('./m4_date.dat', 'w') as outfile:
                outfile.write(str_date_file)

            #pu_file_path = '/user/yuklyushkin/hw1/metrics/{0}/profiles_users.txt'.format(str_date_file)
            #command = TEMPLATE.format(pu_file_path)
            command = TEMPLATE.format(prevfiles)
            result_code = int(os.system(command))
            if result_code != 0:
                print '\n\n*********\n\nERROR\n\n*********\n\n'
                break
            print '\ncomputed\n'

            #dir_path = file_path.split('/')[-2]
            #command = 'hdfs dfs -cp out/part-00000 hw1/metrics/{0}/hw3_1.txt'.format(dir_path)
            #result_command = int(os.system(command))
            #if result_command != 0:
            #    print '\n\n++++++++++\n\nERROR\n\n++++++++++\n\n'
            #    break
            add_dir_to_file(file_path, DONE_FILES_FILE)
            #break
            
        #break


if __name__ == '__main__':
    main()
