#!/usr/bin/env python


import sys
import re


def main():
    current_key = None
    is_new = False
    is_was_before = False
    is_facebook = False

    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue

        key, value = line.split('\t')

        if current_key is None:
            current_key = key
            is_new = False
            is_was_before = False
            is_facebook = False

            if value == '1':
                is_was_before = True

            elif value == '2':
                is_new = True

            elif value == '3':
                is_facebook = True

            else:
                print 1 / 0

        elif current_key != key:
            if is_new and not is_was_before and is_facebook:
                print current_key

            current_key = key
            is_new = False
            is_was_before = False
            is_facebook = False

            if value == '1':
                is_was_before = True

            elif value == '2':
                is_new = True

            elif value == '3':
                is_facebook = True

            else:
                print 1 / 0

        else:
            if value == '1':
                is_was_before = True

            elif value == '2':
                is_new = True

            elif value == '3':
                is_facebook = True

            else:
                print 1 / 0

    if not current_key is None and is_new and not is_was_before and is_facebook:
        print current_key


if __name__ == '__main__':
    main()
