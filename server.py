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

M4_1_FILE = 'm4_1.txt'

M4_2_FILE = 'm4_2.txt'

M5_FILE = 'm5.txt'

MHW2_1_FILE = 'mhw2_1.txt'

MHW2_2_FILE = 'mhw2_2.txt'


# hw 3
import happybase


HOSTS = ["hadoop2-%02d.yandex.ru" % i for i in xrange(11, 14)]
PROFILES_TABLE = "bigdatashad_yuklyushkin_profiles"
USERS_TABLE = "bigdatashad_yuklyushkin_users"


def connect(table):
    host = random.choice(HOSTS)
    conn = happybase.Connection(host)

    conn.open()


    return happybase.Table(table, conn)
# hw 3


def iterate_between_dates(start_date, end_date):
    span = end_date - start_date
    #print span
    for i in xrange(span.days + 1):
        yield start_date + datetime.timedelta(days=i)


def read_data_by_date(date_in):
    try:
        dir_path = 'metrics/{0}/'.format(date_in.strftime("%Y-%m-%d"))
        print date_in, dir_path

        answer = {}

        if os.path.exists(dir_path):
            if os.path.exists(dir_path + M1_FILE):
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
                            answer[parts[0]] = float(parts[1])

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

            tmp = dir_path + M4_1_FILE
            if os.path.exists(tmp):
                cntrs = {}
                with open(tmp, 'r') as infile:
                    print ''
                    m4_cnt = 0
                    for row in infile.readlines():
                        line = row.strip()
                        if len(line) != 0:
                            print line
                            #pos = line.rfind(' ')
                            #key = line[:pos]
                            #value = line[pos + 1:]
                            #cntrs[key] = int(value)
                            if m4_cnt == 0:
                                answer['new_users'] = int(line)
                            m4_cnt += 1

            tmp = dir_path + M4_2_FILE
            if os.path.exists(tmp):
                cntrs = {}
                with open(tmp, 'r') as infile:
                    print ''
                    m4_cnt = 0
                    for row in infile.readlines():
                        line = row.strip()
                        if len(line) != 0:
                            print line
                            if m4_cnt == 0:
                                answer['lost_users'] = int(line)
                            m4_cnt += 1

            tmp = dir_path + MHW2_1_FILE
            if os.path.exists(tmp):
                referers = {}
                with open(tmp, 'r') as infile:
                    print ''
                    for row in infile.readlines():
                        line = row.strip()
                        if len(line) != 0:
                            print line
                            pos = line.rfind(' ')
                            key = line[:pos]
                            value = line[pos + 1:]
                            #if key != '-':
                            referers[key] = int(value)
                if len(referers) != 0:
                    print 'referers'
                    answer['session_referers'] = referers

            tmp = dir_path + MHW2_2_FILE
            if os.path.exists(tmp):
                referers = {}
                with open(tmp, 'r') as infile:
                    print ''
                    m4_cnt = 0
                    for row in infile.readlines():
                        line = row.strip()
                        if len(line) != 0:
                            print line
                            if m4_cnt == 0:
                                answer['profile_liked_three_days'] = int(line)
                            m4_cnt += 1

            tmp = dir_path + M5_FILE
            if os.path.exists(tmp):
                referers = {}
                with open(tmp, 'r') as infile:
                    print ''
                    m4_cnt = 0
                    for row in infile.readlines():
                        line = row.strip()
                        if len(line) != 0:
                            print line
                            if m4_cnt == 0:
                                answer['facebook_signup_conversion_3'] = float(line)
                            m4_cnt += 1

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
    #print start_date    
    end_date = request.args.get("end_date", None)
    #print end_date
    if start_date is None or end_date is None:
        abort(400)
    start_date = datetime.datetime(*map(int, start_date.split("-")))
    end_date = datetime.datetime(*map(int, end_date.split("-")))

    result = {}
    print '[----------]\n', start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    print '[----------]'
    for date in iterate_between_dates(start_date, end_date):
        print date
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


# hw 3
def log(data_str):
    with open('./server.log', 'a') as outfile:
        outfile.write(data_str)


def read_hw3_data_by_date(date_in, profile, ip):
    answer = {}
    try:
        date_str = date_in.strftime("%Y-%m-%d")
        #print date_str
        key = profile + '_' + date_str
        log(key)
        log('\n')

        log('connect to profiles\n')
        table = connect(PROFILES_TABLE)

        value = table.row(key)
        log(str(value))
        log('\n')

        if 'hits:hits' in value:
            answer['profile_hits'] = [int(dummy) for dummy in value['hits:hits'].split(',')]
            print 'profile_hits', answer['profile_hits'], '\n'
            log('profile_hits - ' + str(answer['profile_hits']) + '\n')
        else:
            answer['profile_hits'] = []

        if 'users:users' in value:
            answer['profile_users'] = [int(dummy) for dummy in value['users:users'].split(',')]
            print 'profile_users', answer['profile_users'], '\n'
            log('profile_users - ' + str(answer['profile_users']) + '\n')
        else:
            answer['profile_users'] = []

        if 'last_three_liked_users:users' in value:            
            answer['profile_last_three_liked_users'] = [dummy for dummy in value['last_three_liked_users:users'].split(',')]
            print 'last_three_liked_users', answer['profile_last_three_liked_users'], '\n'
            log('last_three_liked_users - ' + str(answer['profile_last_three_liked_users']) + '\n')

        else:
            answer['profile_last_three_liked_users'] = []

    except Exception as e:
        log('\n')
        log(str(e))

    try:
        date_str = date_in.strftime("%Y-%m-%d")
        key = ip + '_' + date_str
        log(key)
        log('\n')

        log('connect to users\n')
        table = connect(USERS_TABLE)

        value = table.row(key)
        log(str(value))
        log('\n')

        if 'profiles:profiles' in value:
            answer['user_most_visited_profiles'] = [dummy for dummy in value['profiles:profiles'].split(',')]
            print 'most visited profiles', answer['user_most_visited_profiles'], '\n'
            log('most visited profiles - ' + str(answer['user_most_visited_profiles']) + '\n')
        else:
            answer['user_most_visited_profiles'] = []

    except Exception as e:
        log('\n')
        log(str(e))

    return answer


@app.route("/api/hw3")
def api_hw3():
    log('\n##########\n')
    try:
        log(datetime.datetime.now().strftime("%Y-%m-%d"))
        log('\n')
        log(str(request.args))
        log('\n')
    except Exception as e:
        log(str(e))
        log('\n')
    

    start_date = request.args.get("start_date", None)
    #print start_date
    end_date = request.args.get("end_date", None)
    #print end_date
    profile = request.args.get("profile_id", None)
    #print profile
    ip = request.args.get("user_ip", None)
    #print ip
    if start_date is None or end_date is None or profile is None or ip is None:
        log('some of parameters is None\n')
        abort(400)
    start_date = datetime.datetime(*map(int, start_date.split("-")))
    end_date = datetime.datetime(*map(int, end_date.split("-")))

    result = {}
    print '[----------]\n', start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    print 'hw3\n[----------]'
    for date in iterate_between_dates(start_date, end_date):
        print date
        data = read_hw3_data_by_date(date, profile, ip)
        #total_hits = int(random.normalvariate(1000, 50))
        #total_users = int(random.normalvariate(100, 5))
        result[date.strftime("%Y-%m-%d")] = data#{
        #    "total_hits": total_hits,
        #    "total_users": total_users,
        #}
        print ''

    print '[==========]\n'
    return jsonify(result)
# hw 3


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
