#!/shared/anaconda/bin/python


import sys

import pandas as pd


NOT_FOUNDED = '<NOT FOUNDED>'


sys.path.append('.')

"""countries_list = []
with open('./IP2LOCATION-LITE-DB1.CSV', 'r') as infile:
    for row in infile.readlines():
        line = row.strip() 
        if len(line) != 0:
            line = line.replace('"', '')
            # print line
            parts = line.split(',')
            lower = int(parts[0])
            upper = int(parts[1])
            country = parts[3]
            countries_list.append((lower, upper, country))
# print countries_list[:5]
"""
countries_df = pd.read_csv('./IP2LOCATION-LITE-DB1.CSV', 
                           header=None,
                           names=['lower', 'upper', 'code', 'name'])
    

def to_dec(ip_address):
    byte_0, byte_1, byte_2, byte_3 = map(int, ip_address.split("."))  # 2, 16, 160, 128
    dec = byte_0 << 24 | byte_1 << 16 | byte_2 << 8 | byte_3 << 0  # 34644096
    return dec


def to_ip(dec):
    byte_0 = (dec >> 24) & 0xff  # 2
    byte_1 = (dec >> 16) & 0xff  # 16
    byte_2 = (dec >>  8) & 0xff  # 161
    byte_3 = (dec >>  0) & 0xff  # 255
    ip_address = ".".join(map(str, [byte_0, byte_1, byte_2, byte_3]))
    return ip_address


def which_country(ip_address):
    dec = to_dec(ip_address)
    dummy = countries_df[
                (dec >= countries_df.lower) &
                (dec <= countries_df.upper)]
    if dummy.shape[0] == 0:
        return NOT_FOUNDED
    return dummy.name.item()
    #for row in countries_list:
    #    if dec >= row[0] and dec <= row[1]:
    #        return row[2]
    #return NOT_FOUNDED


if __name__ == '__main__':
    ip_address = '196.223.28.31'
    print ip_address, which_country(ip_address)
