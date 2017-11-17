#!/usr/bin/env python


import sys
import re


sys.path.append('.')
import ipcountry


def main():
    current_key = None
    for line in sys.stdin:
        key, value = line.split()
        if current_key is None:
            current_key = key
        elif current_key != key:
            try:
                country = ipcountry.which_country(ip)
                print current_key
            except:
                pass
            current_key = key

    if not current_key is None:
        try:
            country = ipcountry.which_country(ip)
            print current_key
        except:
            pass


if __name__ == '__main__':
    main()

