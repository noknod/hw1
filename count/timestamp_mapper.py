#!/usr/bin/env python


import sys
import re
import datetime


def main():
    current_key = None
    record_re = re.compile('([\d\.:]+) - - \[(\S+ [^"]+)\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')
    for line in sys.stdin:
        match = record_re.match(line)
        if not match:
            continue
        if match.group(6) != "200":
            continue
        ip_address = match.group(1)
        """ts_str = match.group(2)
        ts = ts_str.split('/')[2].split()[0][5:]
        """
        try:
            ts = datetime.datetime.strptime(match.group(2), "%d/%b/%Y:%H:%M:%S")
        except ValueError:
            continue
        print "%s\t%s" % (ip_address, ts.strftime("%H:%M:%S"))


if __name__ == '__main__':
    main()
