#!/usr/bin/env python


import sys
import os

def extract_fields(line, date_file):
    line = line.strip()
    if len(line) == 0:
        return

    profile, time_str, ip, liked = line.split('\t')
    if liked != 'yes':
        return

    return profile + '_' + date_file + '_' + time_str + '\t' + ip


def main():
    filename = os.environ['map_input_file']
    date_file = filename.split('/')[-2]

    for line in sys.stdin:
        answer = extract_fields(line, date_file)
        if answer is not None:
            print answer


if __name__ == '__main__':
    main()
