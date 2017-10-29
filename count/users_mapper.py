#!/usr/bin/env python


import sys
import re


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
        print ip_address, 1


if __name__ == '__main__':
    main()

