#!/usr/bin/env python


import sys


def main():
    current_key = None
    cnt = 0
    uniq_cnt = 0
    total_hits = 0
    for line in sys.stdin:
        if len(line.strip()) == 0:
            continue
        print line


if __name__ == '__main__':
    main()
