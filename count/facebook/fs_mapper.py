#!/usr/bin/env python


import sys
import os
#import re
#import datetime


#LOG_LINE_RE = re.compile('^([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')


def main():

    sys.path.append('./')
    with open('./dates_users.dat', 'r') as infile:
        use_date_file = infile.read().strip()

    filename = os.environ['map_input_file']
    date_file = filename.split('/')[-2]

    if filename.endswith('signup.txt'):

        if use_date_file == date_file:
            for line in sys.stdin:
                line = line.strip()
                if len(line) == 0:
                    continue

                print line + '\t3'

        else:
            for line in sys.stdin:
                line = line.strip()
                if len(line) == 0:
                    continue

                print line + '\t2'
    else:
        for line in sys.stdin:
            line = line.strip()
            if len(line) == 0:
                continue

            print line + '\t1'


if __name__ == '__main__':
    main()
