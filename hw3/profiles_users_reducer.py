#!/usr/bin/env python


import sys


def main():
    current_key = None
    cnt = 0
    uniq_cnt = 0
    total_hits = 0
    for line in sys.stdin:
        line = line.strip()
        if len(line) != 0:
            print line


if __name__ == '__main__':
    main()
