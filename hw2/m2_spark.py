#!/usr/bin/env python


import os
import datetime
import re

from pyspark import SparkConf, SparkContext


def main():
    conf = SparkConf().setAppName("Hw 2 metric 2 yuklyushkin")
    sc = SparkContext(conf=conf)

    with open('date.txt') as infile:
        date_str = infile.read().strip()
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    
    liked_users = None    
    for day_shift in range(3):
        log_file = "/user/bigdatashad/logs/{0}/access.log.{1}".format(date_str, date_str)
        
        log = sc.textFile(log_file)

        fields = log.map(extract_fields).filter(lambda x: x is not None)

        if liked_users is None:
            liked_users = fields
        else:
            liked_users = liked_users.intersection(fields)
        
        liked_users.persist()

        date -= datetime.timedelta(days=1)

    liked_users_count = liked_users.count()
    with open('../hw1/hw1/metrics/{0}/mhw2_2.txt'.format(date_str), 'w') as outfile:
        outfile.write(liked_users_count)

    sc.stop()


LOG_LINE_RE = re.compile('([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')


def extract_fields(line):
    #print line
    """
    try:
        match = LOG_LINE_RE.search(line.strip())
        if not match:
           return
        if match.group(6) != "200":
            return

        query = words[4]
        #print '\t', query
        resource = query.split()[1]
        if resource.find('?like=') == -1:
            return
        
        return resource.split('?', 1)[0][1:].strip()
    except Exception, e:
        print e
        return
    """
    match = LOG_LINE_RE.search(line.strip())
    if not match:
        return
    if match.group(6) != "200":
        return

    query = words[4]
    #print '\t', query
    resource = query.split()[1]
    if resource.find('?like=') == -1:
        return
        
    return resource.split('?', 1)[0][1:].strip()


if __name__ == "__main__":
    main()
