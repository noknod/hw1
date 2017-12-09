#!/shared/anaconda/bin/python

import sys


def extract_fields(line):
    line = line.strip()
    if len(line) == 0:
        return

    profile, time_str, ip, liked = line.split()
    if liked != 'no':
        return

    hour = time_str.split(':')[0]

    return profile + ' ' + hour


def main():
    for line in sys.stdin:
        answer = extract_fields(line)
        if answer is not None:
            print answer


if __name__ == '__main__':
    main()
