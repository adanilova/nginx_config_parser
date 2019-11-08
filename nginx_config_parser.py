#!/usr/bin/python

import argparse
from os import path
import re
import requests

main_config = "/etc/nginx/nginx.conf"
config_dir = "/etc/nginx/sites-enabled/"

regex_listen = r"^\s*listen\s*((\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|localhost|[*])?[:]?(\d{1,65535})?).*;.*$"
regex_nginx = r"^.*nginx.*$"

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

def parse_nginx(line):
    match = re.match(regex_nginx,line)
    flag = 1 if match != None else 0
    return flag

def ping(ip_address, port):
    response = requests.get("http://{}:{}".format(ip_address, port))
    headers = response.headers
    server = "" if headers.get("Server") == None else headers.get("Server")
    flag = parse_nginx(server)
    return dict(ip_address=ip_address, port=port, flag=flag)


def main():

    output = []

    lines = [line.rstrip('\n') for line in open("test.txt")]
    for line in lines:
        result = parse_listen(line)
        if not result["success"]:
            continue

        ip_address = result["ip_address"] or "0.0.0.0"
        port = result["port"] or "80"

        if ip_address == "*":
            ip_address = "0.0.0.0"

        info = ping(ip_address, port)
        print "{}:{} {}".format(info["ip_address"], info["port"], info["flag"])
        output.append(info)
    return output

if __name__ == "__main__":
    main()
