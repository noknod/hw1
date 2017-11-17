#!/usr/bin/env python


import sys
import os
import re
import datetime


LOG_LINE_RE = re.compile('^([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')


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


def main():

    sys.path.append('./')
    with open('./dates_users.dat', 'r') as infile:
        use_date_file = infile.read().strip()

    filename = os.environ['map_input_file']
    date_file = filename.split('/')[-2]

    if use_date_file == date_file:
    #if filename.endswith('users.txt'):
        #date_file = filename.split('/')[-2]
        for line in sys.stdin:
            line = line.strip()
            if len(line) != 0:
                print line + '\t2' #+ date_file + '\t' + date_file + '\t2'

    else:
        for line in sys.stdin:
            line = line.strip()
            if len(line) != 0:
                print line + '\t1'


if __name__ == '__main__':
    main()
