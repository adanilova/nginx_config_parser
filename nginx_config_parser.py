#!/usr/bin/python

import argparse
from os import path
import re

main_config = "/etc/nginx/nginx.conf"
config_dir = "/etc/nginx/sites-enabled/"

regex_listen = r"^\s*listen\s*((\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|localhost|[*])?[:]?(\d{1,65535})?);.*$"

def parse_listen(line):
    matches = re.match(regex_listen,line)
    if matches:
        ip_address = matches.group(2)
        port = matches.group(3)
        print "IP_ADDRESS: {}    PORT: {}".format(ip_address, port)


def main():
    
    lines = [line.rstrip('\n') for line in open("test.txt")]
    for line in lines:
        parse_listen(line)


if __name__ == "__main__":
    main()
