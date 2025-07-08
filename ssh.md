# SSH远程服务常见问题

## 创建普通用户可以秘钥远程登录服务器

1. 创建用户
```
useradd -m sshuser

选项：
  -b, --base-dir BASE_DIR	新账户的主目录的基目录
  -c, --comment COMMENT         新账户的 GECOS 字段
  -d, --home-dir HOME_DIR       新账户的主目录
  -D, --defaults		显示或更改默认的 useradd 配置
 -e, --expiredate EXPIRE_DATE  新账户的过期日期
  -f, --inactive INACTIVE       新账户的密码不活动期
  -g, --gid GROUP		新账户主组的名称或 ID
  -G, --groups GROUPS	新账户的附加组列表
  -h, --help                    显示此帮助信息并推出
  -k, --skel SKEL_DIR	使用此目录作为骨架目录
  -K, --key KEY=VALUE           不使用 /etc/login.defs 中的默认值
  -l, --no-log-init	不要将此用户添加到最近登录和登录失败数据库
  -m, --create-home	创建用户的主目录
  -M, --no-create-home		不创建用户的主目录
  -N, --no-user-group	不创建同名的组
  -o, --non-unique		允许使用重复的 UID 创建用户
  -p, --password PASSWORD		加密后的新账户密码
  -r, --system                  创建一个系统账户
  -R, --root CHROOT_DIR         chroot 到的目录
  -s, --shell SHELL		新账户的登录 shell
  -u, --uid UID			新账户的用户 ID
  -U, --user-group		创建与用户同名的组
  -Z, --selinux-user SEUSER		为 SELinux 用户映射使用指定 SEUSER
```

2. 更新新加用户密码
```
passwd sshuser
```

3. 生成ssh秘钥
```
ssh-keygen # 生成密匙
cd ~/home/myuser/.ssh # 进入自己用户主目录下的.ssh文件夹
mv id_rsa.pub authorized_keys # id_rsa.pub 改成 authorized_keys
chmod 600 authorized_keys # 修改权限，只能自己可以读写，注意，如果不修改的话，登录不了的
```

4. 修改ssh配置,需要使用root权限
```
vim /etc/ssh/sshd_config

...
PubkeyAuthentication yes #编辑允许公钥登录
AuthorizedKeysFile .ssh/authorized_keys # 编辑公钥位置
```

5. 拷贝私钥到本地，用本地私钥登录远程服务器
```
# 拷贝 /home/user/.ssh/id_rsa 到本地
ssh -P22 sshuser@178.53.89.77 -i ~/Desktop/sshusersshkey/id_rsa #使用本地私钥登录远程服务器
```