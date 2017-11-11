#!/usr/bin/env python


import sys
import os


def main():

    sys.path.append('./')
    with open('./dates_users.dat', 'r') as infile:
        use_date_file = infile.read().strip()

    filename = os.environ['map_input_file']
    date_file = filename.split('/')[-2]

    if use_date_file == date_file:
    #if filename.endswith('users.txt'):
        #date_file = filename.split('/')[-2]
        for line in sys.stdin:
            line = line.strip()
            if len(line) != 0:
                print line + '\t2' #+ date_file + '\t' + date_file + '\t2'

    else:
        for line in sys.stdin:
            line = line.strip()
            if len(line) != 0:
                print line + '\t1'


if __name__ == '__main__':
    main()

