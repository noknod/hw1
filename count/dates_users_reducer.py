#!/usr/bin/env python


import sys
import re


def main():

    current_key = None
    #current_value = None
    #was_new_date = None
    #was_last_date = None
    #date_new_date = None
    #date_last_date = None
    is_new = False
    is_was_before = False

    new_cnt = 0
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        #key, new_date, last_date, value = line.split('\t')
        key, value = line.split('\t')

        if current_key is None:
            current_key = key
            #current_value = int(value)
            is_new = False
            is_was_before = False

            if value == '1':
                #was_new_date = new_date
                #was_last_date = last_date
                is_was_before = True

            elif value == '2':
                #date_new_date = new_date
                #date_last_date = last_date
                is_new = True

            else:
                print 1 / 0

        elif current_key != key:
            #if current_key == 2:
            if is_new and not is_was_before:
                #print key, date_new_date, date_last_date
                new_cnt += 1

            current_key = key
            is_new = False
            is_was_before = False

            if value == '1':
                is_was_before = True

            elif value == '2':
                is_new = True

            else:
                print 1 / 0

        else:
            #current_value += int(value)
            
            if value == '1':
                #was_new_date = new_date
                #was_last_date = last_date
                is_was_before = True

            elif value == '2':
                #date_new_date = new_date
                #date_last_date = last_date
                is_new = True

            else:
                print 1 / 0
        


    if not current_key is None and is_new and not is_was_before:  # and current_value == 2:
        #print current_key, date_new_date, date_last_date
        new_cnt += 1

    print new_cnt


if __name__ == '__main__':
    main()

