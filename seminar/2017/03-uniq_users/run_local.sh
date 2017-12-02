#!/usr/bin/env bash

OUT_DIR=out
NUM_REDUCERS=0 # > 0 to run the Reduce phase
CONFIG="--config /home/agorokhov/conf.empty"

hdfs ${CONFIG} dfs -rm -r -skipTrash ${OUT_DIR}

yarn ${CONFIG} jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="Uniq users step1" \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files mapper_get_user_id.py \
    -mapper "./mapper_get_user_id.py | grep 193.227.136.104" \
    -input in \
    -output ${OUT_DIR}
    #-reducer TODO \

# TODO:
# - run in distributed mode (on the cluster)
# - implement the reducer
