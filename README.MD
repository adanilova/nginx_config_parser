It is my Python assignment.

Script scan `/etc/nginx/nginx.conf`, all **files** in `/etc/nginx/conf.d/` and `/etc/nginx/sites-enabled/` directories (no sub-directories) for port listening. With **psutil** lib find all processes of nginx. Then match all pairs of IP address and port from parsed config files with nginx data. If IP address and port is listening by nginx the flag will be 1, in other case the flag will be 0.

* nginx_config_parser.py - executable script file

Install requirements
```
pip install -r requirements.txt
```

Run script
```
./nginx_config_parser.py
```

For correct working requires **sudo privileges**.
