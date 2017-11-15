#!/usr/bin/env python


import os
import datetime
import re

from pyspark import SparkConf, SparkContext
from operator import add


def main():
    conf = SparkConf().setAppName("User sessions")
    sc = SparkContext(conf=conf)

    with open('date.txt') as infile:
        date_str = infile.read().strip()

    log_file = "/user/bigdatashad/logs/{0}/access.log.{1}".format(date_str, date_str)
    #log_file = "./1.txt"

    print '\n***\n'
    print log_file
    print '\n***\n'

    log = sc.textFile(log_file)

    fields = log.map(extract_fields).filter(lambda x: x is not None)
    #print "**********\nLog rows count: %d\n**********" % fields.count()

    ips_sorted = fields.repartitionAndSortWithinPartitions(8, tuple_partitioner)\
        .map(lambda x: (x[0][0], x[1]))
    ips_grouped = ips_sorted.groupByKey()
    #print ips_grouped.take(10)
    #print '\n***\n'
    #for row in ips_grouped.collect():
    #    print row[0]
    #    for q in row[1]:
    #        print '\t', q
    #print '\n***\n'


    sessions = ips_grouped.flatMapValues(count_referer_sessions)
    #print "**********\nReferers count: %d\n**********" % ips_grouped.count()
    #print sessions.take(10)
    referers = sessions.map(lambda x: x[1]).groupByKey().mapValues(sum)
     
    #for referer in referers.collect():
    #    print referer
    
    #for rerefer in referers.collect():
    #    print referer
    # use sessions.fold(...) to sum for all keys
    #referers.saveAsTextFile('/user/yuklyushkin/hw2/metrics/m1_cur.txt')
    with open('../hw1/hw1/metrics/{0}/mhw2_1.txt'.format(date_str), 'w') as outfile:
        is_was = False
        for referer in referers.collect():
            if is_was:
                outfile.write('\n')
            #print referer[0]
            outfile.write(str(referer[0]))
            outfile.write(' ')
            #print referer[1]
            outfile.write(str(referer[1]))
            is_was = True


LOG_LINE_RE = re.compile('([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')


def extract_fields(line):
    #print line
    try:
        match = LOG_LINE_RE.search(line.strip())
        if not match:
           return
        if match.group(6) != "200":
            return
        ip = match.group(1)
        date = datetime.datetime.strptime(match.group(2), "%d/%b/%Y:%H:%M:%S")
        url = match.group(4)
        referer = match.group(7)
        timestamp = int(date.strftime("%s"))
        #print '\t', referer
        #return ((ip, timestamp), (timestamp, 1))
        return ((ip, timestamp), (timestamp, referer))
    except Exception, e:
        print e
        return


def tuple_partitioner(pair):
    return hash(pair[0])


TIME_TO = 30 * 60


def count_referer_sessions(events):
    #sessions = 0
    #sessions_length = 0
    start_timestamp = None
    last_timestamp = None
    #hits = 0
    last_referer = None
    referers = {}

    for event in events:
        timestamp, referer = event

        if not start_timestamp:
            start_timestamp = last_timestamp = timestamp
            last_referer = referer            

        elif timestamp - last_timestamp > TIME_TO or referer != last_referer:
            #sessions += 1
            #sessions_length += last_timestamp - start_timestamp
            referers[last_referer] = referers.get(last_referer, 0) + 1
            start_timestamp = timestamp
            last_referer = referer

        last_timestamp = timestamp
        #hits = hit # += 1

    #sessions += 1
    #sessions_length += last_timestamp - start_timestamp
    #return (sessions, sessions_length, hits)
    if last_referer is not None:
        referers[last_referer] = referers.get(last_referer, 0) + 1

    return referers.items()



if __name__ == "__main__":
    main()

