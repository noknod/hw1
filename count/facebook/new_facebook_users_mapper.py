#!/usr/bin/env python


import sys
import os
import re
import datetime


LOG_LINE_RE = re.compile('^([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')


def main():

    sys.path.append('./')
    with open('./dates_users.dat', 'r') as infile:
        use_date_file = infile.read().strip()

    filename = os.environ['map_input_file']
    date_file = filename.split('/')[-2]

    if use_date_file == date_file:
        for line in sys.stdin:
            answer = extract_fields(line)
            if answer is None:
                continue

            ip_address = answer[0]
            timestamp = answer[1]
            referer = answer[2]

            result = '{0}\t2{1}_{2}'.format(ip_address, timestamp.strftime("%H:%M:%S"), referer)
            print result

    else:
        for line in sys.stdin:
            line = line.strip()
            if len(line) != 0:
                print line + '\t100:00:00_null'


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

    resource = match.group(4)
    if not resource.startswith('/'):
        return

    try:
        timestamp = datetime.datetime.strptime(match.group(2), "%d/%b/%Y:%H:%M:%S")
    except ValueError:
        return

    referer = match.group(7)
    #if referer.lower().find('facebook') == -1:
    #    return None

    ip_address = match.group(1)

    return (ip_address, timestamp, referer)


if __name__ == '__main__':
    main()
