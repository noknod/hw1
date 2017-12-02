hadoop --config /home/agorokhov/conf.empty jar /opt/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=0 \
    -input in/ \
    -output out/ \
    -mapper env

# mapreduce_map_input_file - input file
# https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html
