#!/usr/bin/env python

import sys
import re
import datetime

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

ZK_QUORUM = "hadoop2-10:2181"
KAFKA_TOPIC = "bigdatashad-csc"
KAFKA_CONSUMER_PREFIX = "spark-streaming-consumer17-"


def filter_success(item):
    return item[2] != 200

def parse_access_log(line):
    record_re = re.compile('([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')

    match = record_re.match(line)
    if not match:
        return None
    code = int(match.group(6))
    ip = match.group(1)
    date = datetime.datetime.strptime(match.group(2), "%d/%b/%Y:%H:%M:%S")
    referer = match.group(7)
    url = match.group(4)

    return (ip, int(date.strftime("%s")), code, url, referer)


def main():
    if len(sys.argv) < 1:
        print >> sys.stderr, "Usage: %s consumer_id" % sys.argv[0]
        exit(1)

    consumer_name = KAFKA_CONSUMER_PREFIX + sys.argv[1]

    sc = SparkContext(appName="SparkStreamingTest")
    ssc = StreamingContext(sc, 60) # batch interval

    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )

    #ssc.checkpoint("checkpoints")

    lines = ssc.socketTextStream("localhost", 9966)
    #stream = KafkaUtils.createStream(ssc, ZK_QUORUM, consumer_name, {KAFKA_TOPIC: 5})


    #lines = stream.map(lambda x: x[1])
    lines.pprint()
    users = lines.map(lambda line : parse_access_log(line)) \
                 .filter(lambda item: filter_success(item)) \
                 .map(lambda item: (item[0], 1)) \
                 .reduceByKey(lambda x, y: x + y)
    print users.count()
    users.pprint()

    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
