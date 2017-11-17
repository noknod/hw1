#!/usr/bin/env python


import sys
import re

# 196.223.28.31 - - [16/Nov/2015:00:00:00 +0400] "GET /photo/manage.cgi HTTP/1.1" 200 0 "-" "Mozilla/6.66"

def main():
    current_key = None
    cnt = 0
    uniq_cnt = 0
    total_hits = 0
    for line in sys.stdin:
        if len(line.strip()) == 0:
            continue
        key, value = line.split()
        total_hits += 1
        if current_key is None:
            current_key = key
            cnt = value
            uniq_cnt += 1
        elif current_key != key:
            # print current_key, cnt
            current_key = key
            cnt = value
            uniq_cnt += 1
        else:
            cnt += value

    #if not current_key is None:
    #    print current_key, cnt
    print 'total_hits', total_hits

    print 'total_users', uniq_cnt


if __name__ == '__main__':
    main()

