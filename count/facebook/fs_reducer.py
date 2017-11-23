#!/usr/bin/env python


import sys
import re


def main():
    current_key = None
    is_new = False
    is_was_before = False
    is_signup = False

    signup_cnt = 0
    total_cnt = 0

    #cnt = 0
    for line in sys.stdin:
        line = line.strip()
        #print line
        #continue
        if len(line) == 0:
            continue

        key, value = line.split('\t')

        if current_key is None:
            current_key = key
            is_new = False
            is_was_before = False
            is_signup = False

            if value == '1':
                is_new = True

            elif value == '2':
                is_was_before = True

            elif value == '3':
                is_signup = True

            else:
                print 1 / 0

        elif current_key != key:
            if is_new and not is_was_before and is_signup:
                signup_cnt += 1

            if is_new:
                total_cnt += 1

            current_key = key
            is_new = False
            is_was_before = False
            is_signup = False

            if value == '1':
                is_new = True

            elif value == '2':
                is_was_before = True

            elif value == '3':
                is_signup = True

            else:
                print 1 / 0

        else:
            if value == '1':
                is_new = True

            elif value == '2':
                is_was_before = True

            elif value == '3':
                is_signup = True

            else:
                print 1 / 0

    if not current_key is None and is_new and not is_was_before and is_signup:
        signup_cnt += 1

    if not current_key is None and is_new:
        total_cnt += 1

    if total_cnt > 0.0:
        print 1.0 * signup_cnt / total_cnt
    else:
        print 0.0


if __name__ == '__main__':
    main()
