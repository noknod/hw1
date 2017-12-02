#!/usr/bin/env bash

OUT_DIR="out"
NUM_REDUCERS=4

hdfs dfs -rm -r -skipTrash ${OUT_DIR}

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="Wordcount step1" \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files mapper.py,reducer.py \
    -mapper mapper.py \
    -reducer reducer.py \
    -input /user/agorokhov/data/wiki_sample \
    -output ${OUT_DIR}

for num in `seq 0 $[$NUM_REDUCERS - 1]`
do
    hdfs dfs -cat ${OUT_DIR}/part-0000$num | head
done

# TODO:
# - turn off the Reduce phase: NUM_REDUCERS=0, investigate the result
