#!/usr/bin/env python


import sys
import re

# 196.223.28.31 - - [16/Nov/2015:00:00:00 +0400] "GET /photo/manage.cgi HTTP/1.1" 200 0 "-" "Mozilla/6.66"

def main():
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


if __name__ == '__main__':
    main()

