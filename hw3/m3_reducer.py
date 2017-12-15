#!/usr/bin/env python


import random
import sys

sys.path.append('./')
with open('./m3_date.dat', 'r') as infile:
    date_file = infile.read().strip()


import happybase

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
TABLE = "bigdatashad_yuklyushkin_users"


def connect():
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    conn.open()

    return happybase.Table(TABLE, conn)


def put(table, ip, date_str, profiles_str):
    key = ip + '_' + date_str

    b = table.batch()
    b.put(key, {"profiles:profiles": profiles_str})

    b.send()


def create_dict():
    answer = {}
    return answer


def sort_and_get_str_from_dict(profiles):
    profile_list = []
    for profile, cnt in profiles.items():
        profile_list.append((cnt, profile,))
    profile_list = sorted(profile_list)

    answer = ' '.join(dummy[1] for dummy in profile_list)
    return answer.strip().replace(' ', ',')


def save_into_hbase(table, ip, profiles):
    profiles_str = sort_and_get_str_from_dict(profiles)

    put(table, ip, date_file, profiles_str)


def main():
    table = connect()

    current_key = None

    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue

        ip, profile = line.split('\t')

        if current_key is None:
            current_key = ip
            profiles = create_dict()

            if profile in profiles:
                profiles[profile] -= 1
            else:
                profiles[profile] = -1

        elif current_key != ip:
            save_into_hbase(table, current_key, profiles)

            current_key = ip
            profiles = create_dict()

            if profile in profiles:
                profiles[profile] -= 1
            else:
                profiles[profile] = -1

        else:
            if profile in profiles:
                profiles[profile] -= 1
            else:
                profiles[profile] = -1

    if not current_key is None:
        save_into_hbase(table, current_key, profiles)


if __name__ == '__main__':
    main()
