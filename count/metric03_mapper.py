#!/shared/anaconda/bin/python


import sys


sys.path.append('.')
import ipcountry


def main():
    current_key = None
    for line in sys.stdin:
        line = line.strip()
        if len(line) != 0:
            ip_address = line
            country = ipcountry.which_country(ip_address)
            print country + '\t1'


if __name__ == '__main__':
    main()

