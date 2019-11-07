#!/usr/bin/python

import re

file_name = "nginx.conf"
regex_address = r"\s*(\w?.*)\s*:([0-9]*)[;]"
regex_listen = r".*listen\s*([0-9]*)[;]"
regex_who_is_listening = r".*[{].[#]\s(.*)"
def check_regex(line):
    address_matches = re.match(regex_address,line)
    if address_matches:
        who = address_matches.group(1)
        port = address_matches.group(2)
        message = "Port {} is listening by {}".format(port, who)
        return dict(success=True,listener_unknown=False,message=message)
    listen_matches = re.match(regex_listen,line)
    if listen_matches:
        port = listen_matches.group(1)
        message = "Port {} is listening".format(port)
        return dict(success=True,listener_unknown=True,message=message)
    listener_matches = re.match(regex_who_is_listening,line)
    if listener_matches:
        listener = listener_matches.group(1)
        message = "listener is {}".format(listener)
        return dict(success=False,listener_unknown=False,message=message)
    return dict(success=False,listener_unknown=True,message="")

lines = [line.rstrip('\n') for line in open(file_name)]

previous_message = ""
for line in lines:
    response = check_regex(line)
    if not response["success"]:
        previous_message = response["message"]
        continue
    if response["listener_unknown"]:
        print response["message"] + " " + previous_message
    else:
        print response["message"]
    previous_message = response["message"]
