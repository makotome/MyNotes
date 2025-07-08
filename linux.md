# Linux 学习笔记

#### 一、修改普通用户密码
1. echo newpassword | passwd --stdin username
2. echo username:newpassword | chpasswd

#### 二、chmod命令
在Linux中，一般使用chmod命令来修改文件的属性。利用 chmod 可以藉以控制文件如何被他人所调用。此命令所有使用者都可使用。

1. 查看当前文件夹属性
```
[root@VM_0_17_centos gogs-repositories]# ls -l
总用量 16
drwxr-xr-x 2 git  git  4096 12月 18 14:14 eric
drwxrwxrwx 3 root root 4096 12月  9 19:30 lovecoder
drwxrwxrwx 2 root root 4096 12月  9 19:30 ouyangkan
drwxrwxrwx 4 root root 4096 12月 18 14:06 xumingxin
```
drwxr-xr-x 一共有10位数，其中：最前面1位 d 代表的是类型，接下来3位 rwx 代表的是所有者（user）拥有的权限，再接下来3位 r-x 代表的是组群（group）拥有的权限，最后3位 r-x 代表的是其他人（other）拥有的权限;

2. 跟属性相关简写

* 用户组字母
	- u 表示该文件的拥有者
	- g 表示与该文件的拥有者属于同一个群体(group)者
	- o 表示其他以外的人
	- a 表示这三者皆是

* 权限字母
	- r 表示文件可以被读（read）
	- w 表示文件可以被写（write）
	- x 表示文件可以被执行（如果它是程序的话）
	- \- 表示相应的权限还没有被授予

3. 跟操作相关
先来看一段命名操作
```
chmod a+wrx gogs-bak
```
要看懂上面命令的意思首先需要理解跟操作有关的简写：

* \+ 表示添加权限
* \- 表示删除权限
* = 表示使之成为唯一的权限

上面的命令意思代码给所有用户组增加读写运行的操作。

4. 数字来表示权限
文件和目录的权限表示，是用rwx这三个字符来代表所有者、用户组和其他用户的权限。有时候，字符似乎过于麻烦，因此还有另外一种方法是以数字来表示权限，而且仅需三个数字：

* rwx也可以用数字来代替
	- r: 对应数值4
	- w: 对应数值2
	- x：对应数值1
	- －：对应数值0
* 我们将rwx看成二进制数，如果有则有1表示，没有则有0表示，那么rwx r-x r- -则可以表示成为：111 101 100再将其每三位转换成为一个十进制数，就是754；
* 也可以将其简单的理解为一种运算: (4+2+1) (4+1) (4) = 754

#### 三、修改文件用户所属
```
chown -R git filename
```
chown => change owner的简写， 修改文件的所有者。

```
chgrp： -R git filename
```
chgrp： change group的简写，修改文件所属的用户组。

```
chown -R git:git filename
```
将所有者和组名称都修改为git。

-R => 递归，将子目录下文件全部修改。

#### 四、增加普通用户并设置密码
```
useradd -m username ===>增加用户
passwd usernam ===>修改密码
userdel -r username ===>删除用户
```

#### 5、远程拷贝文件
```
scp -P22 root@4.53.23.77:/root/.ssh/id_rsa ./

scp -P22 username@(IP):srcpath dstpath
```


