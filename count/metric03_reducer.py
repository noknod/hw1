#!/usr/bin/env python


import sys


def main():
    current_key = None
    cnt = 0
    #w = 0
    for line in sys.stdin:
       #w += 1
        key, value = line.strip().split('\t')
        #print 'line', line
        #print 'key', key
        #print 'value', value
        #print '---'
        value = int(value)
        #print key, value

        if current_key is None:
            current_key = key
            cnt = value
        elif current_key != key:
            print current_key, cnt
            current_key = key
            cnt = value
        else:
            cnt += value
        #if w >= 100:
        #    break

    if not current_key is None:
        print current_key, cnt


if __name__ == '__main__':
    main()

