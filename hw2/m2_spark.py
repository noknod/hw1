#!/usr/bin/env python


import os
import re

from datetime import datetime
from datetime import timedelta

from pyspark import SparkConf, SparkContext


START_DATE = datetime.strptime('2017-09-01', '%Y-%m-%d').date()


def main():
    conf = SparkConf().setAppName("Hw 2 metric 2 yuklyushkin")
    sc = SparkContext(conf=conf)

    with open('date.txt') as infile:
        date_str = infile.read().strip()
    date_file = datetime.strptime(date_str, "%Y-%m-%d").date()

    begin_date = date_file + timedelta(days=-2)
    if begin_date < START_DATE:
        begin_date = START_DATE 
    print(date_file, begin_date)
    
    log_file_dates = ['/user/bigdatashad/logs/{0}/access.log.{1}'.format(date_str, date_str)]
    for n in range(int((date_file - begin_date).days)):
                dummy = begin_date + timedelta(n)
                dummy = dummy.strftime('%Y-%m-%d')
                log_file_dates.append(
                    '/user/bigdatashad/logs/{0}/access.log.{1}'.format(dummy, dummy))
    print(log_file_dates)

    """with open('1.txt', 'r') as infile:
        cnt = 0
        for line in infile.readlines():
            line = line.strip()
            if len(line) != 0:
                extract_fields(line)
            cnt += 1
            if cnt == 10:
                break
    """

    first_day_log = sc.textFile(log_file_dates[0])
    second_day_log = sc.textFile(log_file_dates[1])
    third_day_log = sc.textFile(log_file_dates[2])

    first_users = first_day_log.map(extract_fields).filter(lambda x: x is not None).distinct()
    second_users = second_day_log.map(extract_fields).filter(lambda x: x is not None).distinct()
    third_users = third_day_log.map(extract_fields).filter(lambda x: x is not None).distinct()

    liked_users = first_users.intersection(second_users).intersection(third_users)
    """
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
    """

    liked_users_count = liked_users.count()
    #with open('../hw1/hw1/metrics/{0}/mhw2_2.txt'.format(date_str), 'w') as outfile:
    with open('../metrics/{0}/mhw2_2.txt'.format(date_str), 'w') as outfile:
        outfile.write(str(liked_users_count))

    sc.stop()    


LOG_LINE_RE = re.compile('([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')


def extract_fields(line):
    #print '\n', line
    #print('\n', line)
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

    #try:
    #    date_str = datetime.datetime.strptime(match.group(2), "%d/%b/%Y:%H:%M:%S")
    #except:
    #    return

    resource = match.group(4)
    #print '\t', query
    #print('\t', resource)
    if not resource.startswith('/'):
        return

    if resource.find('?like=1') == -1:
        return

    #q = resource.split('?like=1')[0][1:]
    #print(q)
    return resource.split('?like=1')[0][1:].strip()


if __name__ == "__main__":
    main()
