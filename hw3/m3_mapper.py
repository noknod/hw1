#!/usr/bin/env python

import sys


def extract_fields(line):
    line = line.strip()
    if len(line) == 0:
        return

    profile, time_str, ip, liked = line.split('\t')
    if liked == 'yes':
        return

    #if ip != '100.11.10.111':
    #if ip != '9.20.100.231':
    #    return

    return ip + '\t' + profile


def main():
    for line in sys.stdin:
        answer = extract_fields(line)
        if answer is not None:
            print answer


if __name__ == '__main__':
    main()
