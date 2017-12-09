#!/usr/bin/env python
# vim:set et ts=4 sw=4:

import argparse
import calendar
import getpass
import happybase
import logging
import random
import sys


logging.basicConfig(level="DEBUG")

HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
TABLE = "bigdatashad_yuklyushkin_profiles"


def connect():
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    logging.debug("Connecting to HBase Thrift Server on %s", host)
    conn.open()

    logging.debug("Using table %s", TABLE)

    return happybase.Table(TABLE, conn)


#def generate(args, table):
def put(table, profile, date_str, hours_str):
    #for time in get_time_range(args):
    #    b.put(time, {"cf:value": str(random.randint(0, 100000))})
    key = profile + '_' + date_str

    b = table.batch()
    b.put(key, {"hits:hits": hours_str})

    b.send()


def get(table, profile, date_str):
    value = table.row(profile + '_' + date_str)
    print value
    #r = list(get_time_range(args))
    #t = 0L
    #for key, data in table.scan(row_start=min(r), row_stop=max(r)):
    #    if args.total:
    #        t += long(data["cf:value"])
    #    else:
    #        print "%s\t%s" % (key, data["cf:value"])
    #if args.total:
    #    print "total\t%s" % t


def main():
    table = connect()

    #put(table, 'test', '2017-12-09', '1,2,3,4,0,87,2')

    get(table, '1000', '2017-12-01')


if __name__ == "__main__":
    main()
