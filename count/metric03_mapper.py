#!/usr/bin/env python


import sys
import re


sys.path.append('.')
import ipcountry


# 196.223.28.31 - - [16/Nov/2015:00:00:00 +0400] "GET /photo/manage.cgi HTTP/1.1" 200 0 "-" "Mozilla/6.66"

def main():
    current_key = None
    record_re = re.compile('([\d\.:]+) - - \[(\S+ [^"]+)\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')
    #total = 0
    for line in sys.stdin:
        match = record_re.match(line)
        if not match:
            continue
        if match.group(6) != "200":
            continue
        ip_address = match.group(1)
        country = ipcountry.which_country(ip_address)
        print country, 1
        #total += 1
    #print 'total', total


if __name__ == '__main__':
    main()

