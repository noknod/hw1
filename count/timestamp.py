#!/usr/bin/env python


import os
import sys


#    -D mapreduce.job.maps=20 \
TEMPLATE = """
#!/usr/bin/env bash

OUT_DIR=out
NUM_REDUCERS=1 # > 0 to run the Reduce phase
CONFIG="--config /home/agorokhov/conf.empty"

hdfs dfs -rm -r -skipTrash out

yarn jar /opt/hadoop/hadoop-streaming.jar \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapred.text.key.comparator.options=-k1,2 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.text.key.partitioner.options=-k1,1 \
    -D mapreduce.job.reduces=1 \
    -files timestamp_mapper.py \
    -input hdfs://{0} \
    -output out/ \
    -mapper "./timestamp_mapper.py" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -reducer cat
"""

"""jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="Uniq users" \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files timestamp_mapper.py,timestamp_reducer.py \
    -mapper "./timestamp_mapper.py" \
    -reducer "./timestamp_reducer.py" \
    -input hdfs://{0} \
    -output out
"""


ALL_FILES_FILE = '../prepare/data/all_files.txt'

DONE_FILES_FILE = './data/timestamp_files_done.txt'


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
            print(file_path)
            command = TEMPLATE.format(file_path)
            result_code = int(os.system(command))
            if result_code != 0:
                print '\n\n*********\n\nERROR\n\n*********\n\n'
                break
            print '\ncomputed\n'

            dir_path = file_path.split('/')[-2]
            command = 'hdfs dfs -cp out/part-00000 hw1/metrics/{0}/timestamp.txt'.format(dir_path)
            result_command = int(os.system(command))
            if result_command != 0:
                print '\n\n++++++++++\n\nERROR\n\n++++++++++\n\n'
                break
            add_dir_to_file(file_path, DONE_FILES_FILE)
            
        #break


if __name__ == '__main__':
    main()
