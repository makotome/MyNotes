# pip 镜像配置文件

## 配置文件

```bash
vim ~/.pip/pip.conf
```

## 配置内容一本设为阿里云镜像

```conf
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host = mirrors.aliyun.com
```