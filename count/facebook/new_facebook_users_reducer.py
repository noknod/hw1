#!/usr/bin/env python


import sys
import re


def main():
    current_key = None
    is_new = False
    is_was_before = False
    first_referer = None
    first_timestamp = None

    #cnt = 0
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue

        key, info = line.split('\t')
        value = info[0]
        info = info[1:]
        timestamp = info[1:9]
        referer = info[9:]

        if current_key is None:
            current_key = key
            is_new = False
            is_was_before = False
            first_referer = False
            first_timestamp = None

            if value == '1':
                is_was_before = True

            elif value == '2':
                is_new = True
                first_referer = (referer.lower().find('facebook') != -1)
                first_timestamp = timestamp

            else:
                print 1 / 0

        elif current_key != key:
            if is_new and not is_was_before and first_referer:
                print current_key

            current_key = key
            is_new = False
            is_was_before = False
            first_referer = False
            first_timestamp = None

            if value == '1':
                is_was_before = True

            elif value == '2':
                is_new = True
                first_referer = (referer.lower().find('facebook') != -1)
                first_timestamp = timestamp

            else:
                print 1 / 0

        else:
            if value == '1':
                is_was_before = True

            elif value == '2':
                is_new = True
                if first_timestamp is None:
                    first_referer = (referer.lower().find('facebook') != -1)
                    first_timestamp = timestamp
                elif first_timestamp == timestamp:
                    if (referer.lower().find('facebook') != -1):
                        first_referer = True

            else:
                print 1 / 0

    if not current_key is None and is_new and not is_was_before and first_referer:
        print current_key


if __name__ == '__main__':
    main()
