#!/usr/bin/env python


import os
import sys


TEMPLATE = """
#!/usr/bin/env bash

OUT_DIR=out
NUM_REDUCERS=1 # > 0 to run the Reduce phase
CONFIG="--config /home/agorokhov/conf.empty"

hdfs dfs -rm -r -skipTrash out

yarn jar /opt/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.name="KUA HW 3 metric 2" \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapred.text.key.comparator.options=-k1,3 \
    -D stream.num.map.output.key.fields=3 \
    -D mapred.text.key.partitioner.options=-k1,1 \
    -D mapreduce.job.maps=20 \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files m2_mapper.py,m2_reducer.py,m2_date.dat \
    -mapper "./m2_mapper.py" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -reducer "./m2_reducer.py" \
    -input hdfs://{0} \
    -output out
"""

ALL_FILES_FILE = './data/profiles_users_files_done.txt'

DONE_FILES_FILE = './data/m2_files_done.txt'


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
            #if str_date_file > '2017-12-01':
            #    break
            print(file_path)

            with open('./m2_date.dat', 'w') as outfile:
                outfile.write(str_date_file)

            pu_file_path = '/user/yuklyushkin/hw1/metrics/{0}/profiles_users.txt'.format(str_date_file)
            command = TEMPLATE.format(pu_file_path)
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
