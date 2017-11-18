#!/shared/anaconda/bin/python


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
            print current_key
            current_key = key

    if not current_key is None:
        print current_key


if __name__ == '__main__':
    main()

