#!/usr/bin/python

import re

file_name = "nginx.conf"

with open(file_name) as fp:
   line = fp.readline()
   while line:
        print line
