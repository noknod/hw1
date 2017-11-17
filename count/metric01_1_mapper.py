#!/usr/bin/env python


import sys
import re
import datetime


LOG_LINE_RE = re.compile('^([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"$')


def extract_fields(line):
    line = line.strip()
    if len(line) == 0:
        return
    match = LOG_LINE_RE.search(line)    
    if not match:
        return    
    if match.group(6) != "200":
        return
    
    ip = match.group(1)

    date_str = match.group(2)
    try:
        date = datetime.datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S")
    except e:
        return

    resource = match.group(4)
    if not resource.startswith('/'):
        return

    referer = match.group(7)

    time = date.strftime("%H:%M:%S")

    return (ip, time, resource, referer)

# 196.223.28.31 - - [16/Nov/2015:00:00:00 +0400] "GET /photo/manage.cgi HTTP/1.1" 200 0 "-" "Mozilla/6.66"

def main():
    total = 0
    for line in sys.stdin:
        answer = extract_fields(line)
        if not answer is None:
            print answer[0], 1
            total += 1
    #print 'total', total
    """
    current_key = None
    record_re = re.compile('([\d\.:]+) - - \[(\S+ [^"]+)\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')
    total = 0
    for line in sys.stdin:
        #try:
        match = record_re.match(line)
        #except Exception:
        #    is_parsed = False
        #else:
        #    is_parsed = True
        #if not is_parsed:
        #    continue
        if not match:
            continue
        if match.group(6) != "200":
            continue
        print match.group(1), 1
        total += 1
    #print 'total', total
    """


if __name__ == '__main__':
    main()

