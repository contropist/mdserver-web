#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# apt install apache2-utils
# yum -y install httpd-tools
# ab -c 1000 -n 1000000 http://www.zzzvps.com/
# /cc https://www.zzzvps.com/ 120
# ab -c 10 -n 1000 http://t1.cn/wp-admin/index.php
# ab -c 1000 -n 1000000 http://www.zzzvps.com/

python3 index.py

