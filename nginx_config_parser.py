#!/usr/bin/python

from os import path, listdir
import re
import requests
import psutil

# nginx main config files and hosts directories
MAIN_CONFIG = "/etc/nginx/nginx.conf"
CONFIG_DIRS = ["/etc/nginx/conf.d/", "/etc/nginx/sites-enabled/"]

# nginx process program name
NGINX_PROGRAM_NAME = "nginx"

# regex for parse "listen" directive in configs
REGEX_LISTEN = r"^\s*listen\s*(((\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|localhost|[*])[:]?)?(\d{1,65535})?)"


# 1. main script function
def main():
    # all nginx config files path
    files_paths = []
    # check main config file exists and it is a file
    if path.exists(MAIN_CONFIG) and path.isfile(MAIN_CONFIG):
        files_paths.append(MAIN_CONFIG)

    # for each config directory
    for dir_path in CONFIG_DIRS:
        # check hosts directories exist and they are directories
        if not path.exists(dir_path) or not path.isdir(dir_path):
            continue
        # get all directory child files paths
        sub_files_paths = [path.join(dir_path, f) for f in listdir(
            dir_path) if path.isfile(path.join(dir_path, f))]
        # append these files to config files path array
        files_paths = files_paths + sub_files_paths

    # pool of all founded hosts
    hosts_pool = []
    # for each file in nginx config files array
    for file_path in files_paths:
        # all hosts that were parsed in config file
        file_hosts = parse_file(file_path)
        # if there are no hosts - skip to the next file
        if not file_hosts:
            continue
        # append parsed hosts to hosts pool
        hosts_pool.extend(file_hosts)

    # distinct array
    unique_hosts_pool = []
    map(lambda x: not x in unique_hosts_pool and unique_hosts_pool.append(x), hosts_pool)

    # return all founded hosts with nginx owner flag
    return check_for_nginx(unique_hosts_pool)


# 2. parse config file
def parse_file(file_path):
    # all founded hosts in file
    file_hosts = []
    # get all config file lines
    lines = [line.rstrip('\n') for line in open(file_path)]
    # for each line
    for line in lines:
        # parse line to check there is "listen" directive
        host = parse_listen(line)
        # if there is no "listen" directive - skip to the next line
        if not host:
            continue
        # append founded host to config file founded hosts array
        file_hosts.append(host)

    # return all founded hosts
    return file_hosts


# 3. parse line from config file for "listen" directive. Returns None if not parsed
def parse_listen(line):
    # apply regex to the line
    matches = re.match(REGEX_LISTEN, line)
    # return None if there is no matches
    if not matches:
        return None
    # set ip_address from group, if there is None set to default
    ip_address = matches.group(3) or "0.0.0.0"
    # set port from group, if there is None set to default
    port = matches.group(4) or "80"
    # handle another default ip_address value
    if ip_address == "*":
        ip_address = "0.0.0.0"

    # return parsed host
    return dict(ip_address=ip_address, port=port)


# 4. check hosts in hosts pool is nginx process listening them
def check_for_nginx(hosts_pool):
    # result output
    result = []
    # all hosts that nginx process is listening
    nginx_hosts = get_nginx_hosts()

    # for each host in parsed hosts pool
    for host in hosts_pool:
        # flag host was found in nginx hosts
        flag = False

        # check nginx listen 0.0.0.0 with same port
        if dict(ip_address="0.0.0.0", port=host["port"]) in nginx_hosts:
            flag = 1
        else:
            # check nginx listen host ip_address and port
            flag = 1 if host in nginx_hosts else 0

        print_host(host, flag)
        result.append(dict(host=host, flag=flag))

    return result


# 5. get all hosts that nginx process is listening
def get_nginx_hosts():
    nginx_hosts = []
    # get all net connections
    connections = psutil.net_connections()

    # for each connection
    for connection in connections:
        # try to get nginx host from net connection
        nginx_host = get_nginx_host(connection)
        # if nginx_host is None - skip to the next connection
        if not nginx_host:
            continue
        # append nginx_host to nginx hosts array
        nginx_hosts.append(nginx_host)

    return nginx_hosts


# 6. get host from nginx net connection. Returns None if not nginx process
def get_nginx_host(connection):
    # get connection PID, check for None
    pid = connection.pid
    if not pid:
        return None
    # get full process info by PID
    process = psutil.Process(pid)
    if not process:
        return None
    # get process program name
    programm = process.name()
    if programm != NGINX_PROGRAM_NAME:
        return None
    # get local ip_address
    ip_address = connection.laddr.ip
    # get local port
    port = "{}".format(connection.laddr.port)

    # return nginx host
    return dict(ip_address=ip_address, port=port)


# 7. print host result output
def print_host(host, flag):
    print "{}:{} {}".format(host["ip_address"], host["port"], flag)


# main script scope
if __name__ == "__main__":
    main()
