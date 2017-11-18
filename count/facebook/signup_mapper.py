#!/usr/bin/env python


import sys
import os
import re


LOG_LINE_RE = re.compile('^([\d\.:]+) - - \[(\S+) [^"]+\] "(\w+) ([^"]+) (HTTP/[\d\.]+)" (\d+) \d+ "([^"]+)" "([^"]+)"')


def main():
    for line in sys.stdin:
        ip_address = extract_fields(line)
        if ip_address is None:
            continue

        print ip_address


def extract_fields(line):
    #print '\n', line
    #print('\n', line)
    """
    try:
        match = LOG_LINE_RE.search(line.strip())
        if not match:
           return
        if match.group(6) != "200":
            return

        query = words[4]
        #print '\t', query
        resource = query.split()[1]
        if resource.find('?like=') == -1:
            return
        
        return resource.split('?', 1)[0][1:].strip()
    except Exception, e:
        print e
        return
    """
    match = LOG_LINE_RE.search(line.strip())
    if not match:
        return
    if match.group(6) != "200":
        return

    #resource = match.group(4)
    #if not resource.startswith('/'):
    #    return

    url = match.group(4)
    if url.lower().find('/signup') == -1:
        return

    ip_address = match.group(1)

    return ip_address


if __name__ == '__main__':
    main()
