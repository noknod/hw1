#!/usr/bin/env python


import sys
import os
import re


def main():
    filename = os.environ['map_input_file']
    date_file = filename.split('/')[-2]

    if filename == 'total_signup.txt':
        for line in sys.stdin:
            line = line.strip()
            if len(line) != 0:
                print line + '\t1'

    elif filename == 'signup.txt':
        for line in sys.stdin:
            line = line.strip()
            if len(line) != 0:
                print line + '\t2'

    else:
        for line in sys.stdin:
            line = line.strip()
            if len(line) != 0:
                print line + '\t3'
