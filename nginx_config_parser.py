#!/usr/bin/python

from os import path, listdir
import re
import requests

main_config = "/etc/nginx/nginx.conf"
config_dirs = ["/etc/nginx/conf.d/", "/etc/nginx/sites-enabled/"]

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
    response = None
    try:
        response = requests.get("http://{}:{}".format(ip_address, port), timeout=1)
    except:
        return dict(ip_address=ip_address, port=port, flag="Error")
    headers = response.headers
    server = "" if headers.get("Server") == None else headers.get("Server")
    flag = parse_nginx(server)
    return dict(ip_address=ip_address, port=port, flag=flag)

def parse_file(file_path):
    file_results = []
    lines = [line.rstrip('\n') for line in open(file_path)]
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
        file_results.append(info)
    return file_results

def main():
    output = []
    files_paths = [main_config]

    for dir_path in config_dirs:
        abspath = path.abspath(dir_path)
        if path.exists(abspath) == False or path.isdir(abspath) == False:
            continue
        sub_files_paths = [path.join(abspath, f) for f in listdir(abspath) if path.isfile(path.join(abspath, f))]
        files_paths = files_paths + sub_files_paths
    
    for file_path in files_paths:
        file_results = parse_file(file_path)
        if not file_results:
            continue
        output.append(file_results)

    return output

if __name__ == "__main__":
    main()
