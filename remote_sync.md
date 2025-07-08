#!/bin/bash
# 发布 jwwqp.com/agent/two 里面的网页文件
set -x

# 注意除非非常确定，一般不增加 --delete 选项
# rsync -avPe'ssh -p2022' --exclude="*DS_Store*" two/ yafef@47.167.14.72:/data/app/gyzj/nginx/html/agent/two/ $*
# rsync -av host::src /dest
# rsync -avPe'ssh' --exclude={*DS_Store*,logs} rsync-test/ root@167.53.239.77:/root/rsync-test/
# exclude 多种matching pattern
# 第一种写法
# rsync -avzP --exclude *.pth --exclude *.pkl \
# username@xxx.xxx.xxx.xxx:/home/username/your_dirpath/ \
# /home/your_localdir/

# 第二种写法
# rsync -avzP --exclude={*.pth,*.pkl} \ 
# username@xxx.xxx.xxx.xxx:/home/username/your_dirpath/ \
# /home/your_localdir/

# 第三种写法
# rsync -avzP --exclude-from exclude_file.txt \ 
# username@xxx.xxx.xxx.xxx:/home/username/your_dirpath/ \
# /home/your_localdir/

# exclude_file.txt文件中可以写想要排除的文件匹配模式，例如：

# *.pth
# *.pkl


rsync -avPe'ssh -p2022' --exclude={*DS_Store*,logs,data_2020*} yafef@47.167.14.72:/data/app/gyzj/agent_01/ ./agent_01/ $*




#!/usr/bin/python
# -*- coding: UTF-8 -*-
#from __future__ import unicode_literals
import sys
import os

#主机 sshs1.garff3.com 端口 20
#用户密码 xumx ayBXqdnffQ34ZE
# print("#输入用户密码 xumx ayBdddXqdnQ34ZE!")
# os.system("scp -P 2022 /Users/xumingxin/Desktop/gyzj_ios.ipa xumx@sshs1.gar3.com:/usr/share/nginx/html/xumx/")

# 132.78.23.28 / 22
# 资源服务器
# 132.78.23.28 / 22
# xm / xm!@#123
# nginx文件路径: /home/osc/svn/openresty/nginx/xmdir
print("#输入用户密码 xem xm!@we#123!")
# os.system("scp -P 22 /Users/xumingxin/Documents/EgretProjects/wwgame_wx/wwgame_wxgame_remote/resource/wwmj_res.zip xm@10.78.16.28:/home/osc/svn/openresty/nginx/xmdir")

os.system("ssh -p22 xm@132.78.23.28")
