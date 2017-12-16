#!/usr/bin/env python


import random
import sys

sys.path.append('./')
with open('./m4_date.dat', 'r') as infile:
    date_file = infile.read().strip()


import happybase

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
TABLE = "bigdatashad_yuklyushkin_profiles"

def connect():
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    conn.open()

    return happybase.Table(TABLE, conn)


def put(table, profile, date_str, users_str):
    key = profile + '_' + date_str

    b = table.batch()
    b.put(key, {"last_three_liked_users:users": users_str})

    b.send()


class ProfileLastThreeLikedUsers:
    def __init__(self):
        self.__users = {1: None, 2: None, 3: None}
        self.__count = 0

    def push(self, ip):
        self.__users[3] = self.__users[2]
        self.__users[2] = self.__users[1]
        self.__users[1] = ip

        if self.__count < 3:
            self.__count += 1

    def get_str(self):
        answer = ''
        for index in range(1, self.__count + 1):
            answer += ' ' + self.__users[index]

        return answer.strip().replace(' ', ',')


def save_into_hbase(table, profile, users):
    users_str = users.get_str()

    put(table, profile, date_file, users_str)


def main():
    table = connect()

    current_key = None

    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue

        key, ip = line.split('\t')
        profile, date_file, time_str = key.split('_')

        if current_key is None:
            current_key = profile
            users = ProfileLastThreeLikedUsers()

            users.push(ip)

        elif current_key != profile:
            save_into_hbase(table, current_key, users)

            current_key = profile
            users = ProfileLastThreeLikedUsers()

            users.push(ip)

        else:
            users.push(ip)

    if not current_key is None:
        save_into_hbase(table, current_key, users)


if __name__ == '__main__':
    main()
