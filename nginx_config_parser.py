#!/usr/bin/python

import argparse
from os import path
import re

main_config = "/etc/nginx/nginx.conf"
config_dir = "/etc/nginx/sites-enabled/"

regex_listen = r"^\s*listen\s*((\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|localhost|[*])?[:]?(\d{1,65535})?);.*$"

def parse_listen(line):
    matches = re.match(regex_listen,line)
    ip_address = None
    port = None
    success = False
    if matches:
        ip_address = matches.group(2)
        port = matches.group(3)
        success = True
    return dict(ip_address=ip_address, port=port, success=success)


def ping(ip_address, port):
    print "ping {}:{}".format(ip_address, port)


def main():
    
    all_pairs = []

    lines = [line.rstrip('\n') for line in open("test.txt")]
    for line in lines:        
        result = parse_listen(line)
        if not result["success"]:
            continue

        ip_address = result["ip_address"] or "0.0.0.0"
        port = result["port"] or "80"

        ping(ip_address, port)


if __name__ == "__main__":
    main()
