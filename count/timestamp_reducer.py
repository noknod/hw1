#!/usr/bin/env python


import sys
import re


SESSION_TIME_IN_SECONDS = 30 * 60


def main():
    current_key = None

    for line in sys.stdin:
        if len(line.strip()) == 0:
            continue

        parts = line.strip().split('\t')
        #print parts
        key = parts[0]
        hours, minutes, seconds = list(parts[1].split(':'))
        time = int(seconds) + 60 * (int(minutes) + 60 * int(hours))

        if current_key is None:
            session_count = 1
            session_time = 0
            total_count = 0
            bounce_count = 0
            current_key = key

        elif current_key != key:
            session_count += 1            
            current_key = key

        elif time > current_time + SESSION_TIME_IN_SECONDS:
            session_count += 1

        else:
            # old_session_time = session_time
            session_time += time - current_time
            bounce_count += 1
            # if session_time < old_session_time:
            #    print(session_time, old_session_time, time, prev_time)
        current_time = time
        total_count += 1

    if session_count != 0:
        average_session_length = 1.0 * total_count / session_count
        average_session_time = 1.0 * session_time / session_count
        bounce_rate = 1.0 * (session_count - bounce_count) / session_count
    else:
        average_session_length = 0.0
        average_session_time = 0.0
        bounce_rate = 0.0

    print 'average_session_length', average_session_length
    print 'average_session_time', average_session_time
    print 'bounce_rate', bounce_rate
 

if __name__ == '__main__':
    main()

