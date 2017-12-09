#!/usr/bin/env python


import sys


sys.path.append('./')
with open('./m1_date.dat', 'r') as infile:
    date_file = infile.read().strip()


def create_dict():
    answer = {}
    for index in range(24):
        answer[str(index)] = 0
    return answer


def get_str_from_dict(hours):
    answer = ''
    for index in range(24):
        answer += ' ' + str(hours[str(index)])
    return answer.strip().replace(' ', ',')


def save_into_hbase(profile, hours):
    hours_str get_str_from_dict(hours)


def main():
    current_key is None

    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue

        key, value = line.split(' ')

        if current_key is None:
            current_key = key
            hours = create_dict()

        elif current_key != key:
            #print current_key, get_str_from_dict(hours)
            save_into_hbase(current_key, hours)

            current_key = key
            hours = create_dict()
        else:
            hours[value] += 1

    if not current_key is None:
        #print current_key, get_str_from_dict(hours)
        save_into_hbase(current_key, hours)


if __name__ == '__main__':
    main()
