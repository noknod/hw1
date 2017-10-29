#!/usr/bin/env python


import sys
import re


def main():
    current_key = None
    cnt = 0
    for line in sys.stdin:
        key, value = line.split()
        if current_key is None:
            current_key = key
            cnt = value
        elif current_key != key:
            print current_key, cnt
            current_key = key
            cnt = value
        else:
            cnt += value

    if not current_key is None:
        print current_key, cnt


if __name__ == '__main__':
    main()

