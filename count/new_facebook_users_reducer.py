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

    #new_cnt = 0
    #hits = []
    first_referer = None
    cnt = 0
    for line in sys.stdin:
        if cnt <= 100:
            print line
        cnt += 1
        #line = line.strip()
        #if len(line) == 0:
        #    continue
        
        #print line
        #key, new_date, last_date, value = line.split('\t')
        """key, timestamp, referer, value = line.split('\t')

        if current_key is None:
            current_key = key
            #current_value = int(value)
            is_new = False
            is_was_before = False
            #hits = []

            if value == '1':
            #if value.startswith('1'):
                #was_new_date = new_date
                #was_last_date = last_date
                is_was_before = True

            elif value == '2':
            #elif value.startswith('2'):
                #date_new_date = new_date
                #date_last_date = last_date
                is_new = True
                is_first = True
                #dummy = value.split()[1:]
                #hits.append((key, dummy[0], dummy[1]))
                first_referer = (referer.lower().find('facebook') != -1)

            else:
                print 1 / 0

        elif current_key != key:
            #if current_key == 2:
            #if is_new and not is_was_before:
            if is_new and not is_was_before and first_referer:
                #print key, date_new_date, date_last_date
                #new_cnt += 1
                print current_key

                #for row in hits:
                #    print row[0], row[1], row[2]

            current_key = key
            is_new = False
            is_was_before = False
            #hits = []

            if value == '1':
            #if value.startswith('1'):
                is_was_before = True

            elif value == '2':
            #elif value.startswith('2'):
                is_new = True
                #dummy = value.split()[1:]
                #hits.append((key, dummy[0], dummy[1]))
                is_first = True
                first_referer = (referer.lower().find('facebook') != -1)

            else:
                print 1 / 0

        else:
            #current_value += int(value)
            
            if value == '1':
                #was_new_date = new_date
                #was_last_date = last_date
                is_was_before = True

            #elif value == '2':
            elif value.startswith('2'):
                #date_new_date = new_date
                #date_last_date = last_date
                is_new = True
                #dummy = value.split()[1:]
                #hits.append((key, dummy[0], dummy[1]))
                if is_first
                    first_referer = (referer.lower().find('facebook') != -1)
                is_first = False

            else:
                print 1 / 0
        """
        

    """
    #if not current_key is None and is_new and not is_was_before:  # and current_value == 2:
    if not current_key is None and is_new and not is_was_before and first_referer:  # and current_value == 2:
        #print current_key, date_new_date, date_last_date
        #new_cnt += 1
        print current_key
        #for row in hits:
        #    print row[0], row[1], row[2]
    """"

    #print new_cnt


if __name__ == '__main__':
    main()

