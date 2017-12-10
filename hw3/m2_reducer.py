#!/usr/bin/env python
# vim:set et ts=4 sw=4:

import random
import sys

sys.path.append('./')
with open('./m2_date.dat', 'r') as infile:
    date_file = infile.read().strip()


import happybase

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
TABLE = "bigdatashad_yuklyushkin_profiles"


def connect():
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    conn.open()

    return happybase.Table(TABLE, conn)


def put(table, profile, date_str, hours_str):
    key = profile + '_' + date_str

    b = table.batch()
    b.put(key, {"users:users": hours_str})

    b.send()


def create_dict():
    answer = {}
    for index in range(24):
        key = str(index)        
        answer[key.zfill(2)] = 0
    return answer


def get_str_from_dict(hours):
    answer = ''
    for index in range(24):
        key = str(index)
        key = key.zfill(2)
        answer += ' ' + str(hours[key])
    return answer.strip().replace(' ', ',')


def save_into_hbase(table, profile, hours):
    hours_str = get_str_from_dict(hours)

    put(table, profile, date_file, hours_str)


def main():
    table = connect()

    current_key = None
    current_ip = None
    current_hour = None

    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue

        key, value, ip = line.split('\t')

        if current_key is None:
            current_key = key
            current_hour = value
            current_ip = ip
            hours = create_dict()

            hours[value] += 1

        elif current_key != key:
            #print current_key, get_str_from_dict(hours)
            save_into_hbase(table, current_key, hours)
            #print current_key, str(hours)

            current_key = key
            current_hour = value
            current_ip = ip
            hours = create_dict()

            hours[value] += 1     

        else:
            if current_hour != value or current_ip != ip:
                hours[value] += 1

                current_hour = value
                current_ip = ip

    if not current_key is None:
        #print current_key, get_str_from_dict(hours)
        save_into_hbase(table, current_key, hours)
        #print current_key, str(hours)


if __name__ == '__main__':
    main()
