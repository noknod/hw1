#!/usr/bin/env python

import argparse
import datetime
import getpass
import hashlib
import random
import struct

import os
import sys

from flask import Flask, request, abort, jsonify

app = Flask(__name__)
app.secret_key = "my_secret_key"


M1_FILE = 'm1_1_2.txt'

M2_FILE = 'm2.txt'

M3_FILE = 'm3.txt'



def iterate_between_dates(start_date, end_date):
    span = end_date - start_date
    for i in xrange(span.days + 1):
        yield start_date + datetime.timedelta(days=i)


def read_data_by_date(date_in):
    try:
        dir_path = 'metrics/{0}/'.format(date_in.strftime("%Y-%m-%d"))
        print date_in, dir_path

        answer = {}

        if os.path.exists(dir_path):
            with open(dir_path + M1_FILE, 'r') as infile:
                for row in infile.readlines():
                    line = row.strip()
                    if len(line) != 0:
                        print line
                        parts = line.split()
                        answer[parts[0]] = int(parts[1])

            tmp = dir_path + M2_FILE
            if os.path.exists(tmp):
                tses = {}
                with open(dir_path + M2_FILE, 'r') as infile:
                    print ''
                    for row in infile.readlines():
                        line = row.strip()
                        if len(line) != 0:
                            print line
                            parts = line.split()
                            answer[parts[0]] = int(parts[1])

            tmp = dir_path + M3_FILE
            if os.path.exists(tmp):
                cntrs = {}
                with open(tmp, 'r') as infile:
                    print ''
                    for row in infile.readlines():
                        line = row.strip()
                        if len(line) != 0:
                            print line
                            pos = line.rfind(' ')
                            key = line[:pos]
                            value = line[pos + 1:]
                            cntrs[key] = int(value)
                if len(cntrs) != 0:
                    print 'cntrs'
                    answer['users_by_country'] = cntrs

            print answer
        else:
            print '* Not exists *'

        return answer
    except Exception, e:
        print ' *** ERROR ***'
        exc_info = sys.exc_info()
        print exc_info
        return answer


@app.route("/")
def index():
    return "OK!"


@app.route("/api/hw1")
def api_hw1():
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    if start_date is None or end_date is None:
        abort(400)
    start_date = datetime.datetime(*map(int, start_date.split("-")))
    end_date = datetime.datetime(*map(int, end_date.split("-")))

    result = {}
    print '[----------]\n', start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    print '[----------]'
    for date in iterate_between_dates(start_date, end_date):
        data = read_data_by_date(date)
        #total_hits = int(random.normalvariate(1000, 50))
        #total_users = int(random.normalvariate(100, 5))
        result[date.strftime("%Y-%m-%d")] = data#{
        #    "total_hits": total_hits,
        #    "total_users": total_users,
        #}
        print ''

    print '[==========]\n'
    return jsonify(result)


def login_to_port(login):
    """
    We believe this method works as a perfect hash function
    for all course participants. :)
    """
    hasher = hashlib.new("sha1")
    hasher.update(login)
    values = struct.unpack("IIIII", hasher.digest())
    folder = lambda a, x: a ^ x + 0x9e3779b9 + (a << 6) + (a >> 2)
    return 10000 + reduce(folder, values) % 20000


def main():
    parser = argparse.ArgumentParser(description="HW 1 Example")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=login_to_port(getpass.getuser()))
    parser.add_argument("--debug", action="store_true", dest="debug")
    parser.add_argument("--no-debug", action="store_false", dest="debug")
    parser.set_defaults(debug=False)

    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
