It is my Python assignment.

Script scan `/etc/nginx/nginx.conf`, all **files** in `/etc/nginx/conf.d/` and `/etc/nginx/sites-enabled/` directories (no sub-directories) for port listening. Then check response header called `Server`. If header contains `nginx` the flag will be 1, in all other cases the flag will be 0.

* nginx_config_parser.py - executable script file

Install requirements
```
pip install -r requirements.txt
```

Run script
```
./nginx_config_parser.py
```
