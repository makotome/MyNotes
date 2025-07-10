## 查看 CentOS 系统信息

### 查看系统版本和发行版信息

#### 1. 查看 CentOS 版本
```bash
# 方法1：查看发行版信息
cat /etc/redhat-release

# 方法2：查看系统版本详细信息
cat /etc/os-release

# 方法3：查看 CentOS 版本（适用于较新版本）
cat /etc/centos-release
```

#### 2. 查看内核版本
```bash
# 查看内核版本
uname -r

# 查看完整系统信息
uname -a
```

#### 3. 查看系统架构
```bash
# 查看系统架构（32位还是64位）
uname -m
# 或者
arch

# 查看 CPU 信息
lscpu
```

#### 4. 查看系统运行时间和负载
```bash
# 查看系统运行时间和负载
uptime

# 查看系统启动时间
who -b
```

#### 5. 查看可用的包管理器
```bash
# 检查是否有 yum
which yum

# 检查是否有 dnf
which dnf

# 查看 yum 版本
yum --version

# 查看 dnf 版本（如果可用）
dnf --version
```

#### 6. 综合系统信息查看
```bash
# 显示主机名
hostname

# 显示完整的系统信息
hostnamectl

# 查看系统服务管理器类型
ps --no-headers -o comm 1
```

### 示例输出解读

#### CentOS 7 示例输出：

```
$ cat /etc/redhat-release
CentOS Linux release 7.9.2009 (Core)

$ uname -r
3.10.0-1160.el7.x86_64
```

#### CentOS 8 示例输出：
```
$ cat /etc/redhat-release
CentOS Linux release 8.4.2105

$ uname -r
4.18.0-305.el8.x86_64
```

#### CentOS 9 示例输出：
```
$ cat /etc/redhat-release
CentOS Stream release 9

$ uname -r
5.14.0-70.el9.x86_64
```

## 安装JDK21，设置JDK环境变量

### 使用 yum/dnf 包管理器安装（推荐）

#### 1. 更新系统包
```bash
# CentOS 7
sudo yum update -y

# CentOS 8/9 (使用 dnf)
sudo dnf update -y
```

#### 2. 安装 JDK 21
```bash
# CentOS 7
sudo yum install -y java-21-openjdk java-21-openjdk-devel

# CentOS 8/9
sudo dnf install -y java-21-openjdk java-21-openjdk-devel
```

#### 3. 验证安装
```bash
java -version
javac -version
```

### 故障排除：如果找不到 java-21-openjdk 包

如果遇到 "未找到匹配的参数: java-21-openjdk" 错误，可以尝试以下解决方案：

#### 方案1：查看可用的 Java 版本
```bash
# 查看系统可用的 Java 包
yum search openjdk

# 或者使用 dnf（如果可用）
dnf search openjdk

# 列出所有可用的 Java 相关包
yum list | grep openjdk
```

#### 方案2：启用 EPEL 仓库（推荐）
```bash
# 安装 EPEL 仓库
sudo yum install -y epel-release

# 更新包列表
sudo yum update

# 再次尝试安装 JDK 21
sudo yum install -y java-21-openjdk java-21-openjdk-devel
```

#### 方案3：安装可用的最新 OpenJDK 版本
```bash
# 查看可用的 Java 版本
yum list available | grep openjdk

# 通常可用的版本（根据实际情况选择）
sudo yum install -y java-11-openjdk java-11-openjdk-devel
# 或者
sudo yum install -y java-17-openjdk java-17-openjdk-devel
# 或者
sudo yum install -y java-1.8.0-openjdk java-1.8.0-openjdk-devel
```

#### 方案4：手动下载安装 JDK 21

##### 4.1 下载 OpenJDK 21
```bash
# 创建安装目录
sudo mkdir -p /opt/java

# 下载 OpenJDK 21 (Eclipse Temurin)
cd /tmp
wget https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3%2B9/OpenJDK21U-jdk_x64_linux_hotspot_21.0.3_9.tar.gz

# 或者下载 Oracle JDK 21（需要接受许可协议）
# wget https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.tar.gz
```

##### 4.2 解压并安装
```bash
# 解压到安装目录
sudo tar -xzf OpenJDK21U-jdk_x64_linux_hotspot_21.0.3_9.tar.gz -C /opt/java/

# 创建软链接
sudo ln -s /opt/java/jdk-21.0.3+9 /opt/java/jdk21

# 设置权限（设置所有者和用户组）
sudo chown -R root:root /opt/java/jdk21

# chown 命令详解：
# sudo: 以管理员权限执行
# chown: change owner 的缩写，用于改变文件/目录的所有者
# -R: recursive，递归处理，包括所有子目录和文件
# root:root: 第一个root是所有者(owner)，第二个root是用户组(group)
# /opt/java/jdk21: 要修改权限的目标路径
```

##### 4.3 设置环境变量
```bash
# 编辑环境配置文件
sudo nano /etc/profile

# 添加以下内容到文件末尾
export JAVA_HOME=/opt/java/jdk21
export JRE_HOME=$JAVA_HOME
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH

# 环境变量详解：
# JAVA_HOME: JDK 安装根目录
# JRE_HOME: JRE 运行环境目录
# CLASSPATH: Java 类路径，告诉 JVM 在哪里查找类文件
#   . : 表示当前目录（重要！）
#   : : 路径分隔符（Linux/Unix 使用冒号，Windows 使用分号）
#   $JAVA_HOME/lib : JDK 核心库目录
#   $JRE_HOME/lib : JRE 运行库目录
# PATH: 系统可执行文件搜索路径
#   $JAVA_HOME/bin : 新增的Java可执行文件目录（java, javac, jar等）
#   $PATH : 保留原有的系统PATH路径
#   这样做是为了在原有PATH基础上添加Java路径，而不是覆盖

# PATH 详细解释：
# export PATH=$JAVA_HOME/bin:$PATH
# 这行命令的含义：
# 1. $JAVA_HOME/bin : Java可执行文件目录（包含java, javac, jar等命令）
# 2. : : 路径分隔符
# 3. $PATH : 系统原有的PATH环境变量
# 4. 最终效果：在原有PATH前面添加Java路径，优先使用我们安装的Java

# 为什么这样设置？
# - 如果只设置 PATH=/opt/java/jdk21/bin，会丢失所有系统原有路径
# - 如果设置 PATH=$PATH:$JAVA_HOME/bin，Java路径在后面，可能被系统自带Java覆盖
# - 设置 PATH=$JAVA_HOME/bin:$PATH，Java路径在前面，优先级最高

# 使配置生效
source /etc/profile
```

#### 权限说明和多用户使用

##### 权限解读
```bash
# 查看 JDK 安装目录权限
ls -la /opt/java/

# 权限示例解读：
# lrwxrwxrwx 1 root root  20 7月   9 11:48 jdk21 -> /opt/java/jdk-21.0.7
# drwxr-xr-x 9 root root 136 7月   9 11:47 jdk-21.0.7
```

**权限解释：**
- `lrwxrwxrwx`：软链接，所有用户都可以读取和执行
- `drwxr-xr-x`：目录权限
  - `d`：表示目录
  - `rwx`：所有者（root）可读、写、执行
  - `r-x`：组用户可读、执行（不能写）
  - `r-x`：其他用户可读、执行（不能写）

##### 多用户使用配置

**当前权限下的使用情况：**
```bash
# ✅ 所有用户都可以使用 Java 命令（如果环境变量配置正确）
# ✅ 所有用户都可以读取 JDK 文件
# ❌ 只有 root 用户可以修改 JDK 安装目录
```

**为所有用户配置 Java 环境：**

1. **全局环境变量配置（推荐）**
```bash
# 编辑全局配置文件
sudo nano /etc/profile

# 确保包含以下内容
export JAVA_HOME=/opt/java/jdk21
export JRE_HOME=$JAVA_HOME
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH

# 使所有用户生效
sudo chmod +x /etc/profile
```

2. **为系统所有用户创建脚本**
```bash
# 创建 Java 环境脚本
sudo nano /etc/profile.d/java.sh

# 添加内容
#!/bin/bash
export JAVA_HOME=/opt/java/jdk21
export JRE_HOME=$JAVA_HOME
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH

# 设置可执行权限
sudo chmod +x /etc/profile.d/java.sh
```

3. **验证其他用户可以使用**
```bash
# 切换到普通用户测试
su - username  # 替换为实际用户名

# 或者创建测试用户
sudo useradd testuser
sudo passwd testuser
su - testuser

# 检查 Java 是否可用
java -version
javac -version
echo $JAVA_HOME
```

##### 如果需要给特定用户组更多权限

**创建 Java 用户组并设置权限：**
```bash
# 创建 java 用户组
sudo groupadd java

# 将用户添加到 java 组
sudo usermod -a -G java username

# 修改 JDK 目录的组权限
sudo chgrp -R java /opt/java/jdk21
sudo chmod -R g+w /opt/java/jdk21/temp  # 如果需要写入临时文件

# 查看修改后的权限
ls -la /opt/java/
```

##### 常见用户权限问题解决

**问题1：普通用户找不到 java 命令**
```bash
# 解决方案：检查 PATH 环境变量
echo $PATH | grep java

# 如果没有，重新加载环境变量
source /etc/profile
# 或者重新登录用户
```

**问题2：权限不足错误**
```bash
# 检查文件权限
ls -la /opt/java/jdk21/bin/java

# 如果权限不够，修复权限
sudo chmod +x /opt/java/jdk21/bin/*
```

**问题3：临时文件写入权限**
```bash
# Java 可能需要在临时目录写入文件
sudo mkdir -p /opt/java/jdk21/temp
sudo chmod 1777 /opt/java/jdk21/temp  # 所有用户可读写，但只能删除自己的文件
```

##### 安全建议

**推荐的权限设置：**
```bash
# JDK 主目录：只有 root 可写，所有用户可读可执行
sudo chmod -R 755 /opt/java/jdk21

# 可执行文件：所有用户可执行
sudo chmod +x /opt/java/jdk21/bin/*

# 配置文件：只读
sudo chmod -R 644 /opt/java/jdk21/conf/
sudo chmod -R 644 /opt/java/jdk21/lib/
```

**用户级配置（可选）：**
```bash
# 如果某个用户需要自定义 Java 配置
echo 'export JAVA_HOME=/opt/java/jdk21' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```


## 安装Maven，设置Maven环境变量

### 前提条件
确保已经安装并配置好 JDK（Maven 需要 Java 环境）：
```bash
# 验证 Java 是否已安装
java -version
echo $JAVA_HOME
```

### 方法一：使用包管理器安装（推荐）

#### 1. 使用 yum/dnf 安装 Maven
```bash
# CentOS 7
sudo yum install -y maven

# CentOS 8/9
sudo dnf install -y maven

# 安装开发工具包（包含 Maven）
sudo yum groupinstall -y "Development Tools"
```

#### 2. 验证安装
```bash
mvn -version
```

### 方法二：手动下载安装最新版本

#### 2.1 下载 Maven
```bash
# 创建安装目录
sudo mkdir -p /opt/maven

# 下载最新版本的 Maven（以 3.9.6 为例）
cd /tmp
wget https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz

# 或者使用国内镜像加速下载
wget https://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz
```

#### 2.2 解压并安装
```bash
# 解压到安装目录
sudo tar -xzf apache-maven-3.9.6-bin.tar.gz -C /opt/maven/

# 创建软链接方便管理
sudo ln -s /opt/maven/apache-maven-3.9.6 /opt/maven/latest

# 设置权限
sudo chown -R root:root /opt/maven/
sudo chmod -R 755 /opt/maven/
```

#### 2.3 设置环境变量

##### 全局配置（推荐）
```bash
# 编辑全局环境配置
sudo nano /etc/profile

# 在文件末尾添加以下内容：
export M2_HOME=/opt/maven/latest
export M2=$M2_HOME/bin
export MAVEN_HOME=/opt/maven/latest
export PATH=$M2:$PATH

# 使配置生效
source /etc/profile
```

##### 或者使用 profile.d 配置
```bash
# 创建 Maven 环境脚本
sudo nano /etc/profile.d/maven.sh

# 添加以下内容：
#!/bin/bash
export M2_HOME=/opt/maven/latest
export M2=$M2_HOME/bin
export MAVEN_HOME=/opt/maven/latest
export PATH=$M2:$PATH

# 设置可执行权限
sudo chmod +x /etc/profile.d/maven.sh

# 重新加载环境变量
source /etc/profile.d/maven.sh
```

#### 2.4 验证安装
```bash
# 检查 Maven 版本
mvn -version

# 检查环境变量
echo "M2_HOME: $M2_HOME"
echo "MAVEN_HOME: $MAVEN_HOME"
echo "PATH: $PATH"

# 查看 Maven 命令位置
which mvn
```

### Maven 配置优化

#### 3.1 配置国内镜像源（提高下载速度）
```bash
# 编辑 Maven 配置文件
sudo nano /opt/maven/latest/conf/settings.xml

# 或者创建用户级配置
mkdir -p ~/.m2
nano ~/.m2/settings.xml
```

在 `<mirrors>` 标签内添加阿里云镜像：
```xml
<mirror>
    <id>aliyunmaven</id>
    <mirrorOf>*</mirrorOf>
    <name>阿里云公共仓库</name>
    <url>https://maven.aliyun.com/repository/public</url>
</mirror>
```

#### 3.2 配置本地仓库路径
```bash
# 创建本地仓库目录
sudo mkdir -p /opt/maven/repository
sudo chown -R $USER:$USER /opt/maven/repository

# 在 settings.xml 中配置本地仓库路径
# 在 <settings> 标签内添加：
# <localRepository>/opt/maven/repository</localRepository>
```

### 环境变量详解

```bash
# Maven 环境变量说明：
# M2_HOME: Maven 安装根目录
# M2: Maven 的 bin 目录路径
# MAVEN_HOME: Maven 安装根目录（与 M2_HOME 相同）
# PATH: 添加 Maven 的 bin 目录到系统路径

export M2_HOME=/opt/maven/latest
export M2=$M2_HOME/bin
export MAVEN_HOME=/opt/maven/latest
export PATH=$M2:$PATH
```

### 测试 Maven 安装

#### 4.1 创建测试项目
```bash
# 创建工作目录
mkdir -p ~/maven-test
cd ~/maven-test

# 使用 Maven 创建简单项目
mvn archetype:generate -DgroupId=com.example.test -DartifactId=maven-test-project -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

# 进入项目目录
cd maven-test-project

# 编译项目
mvn compile

# 运行测试
mvn test

# 打包项目
mvn package
```

#### 4.2 验证项目构建
```bash
# 查看生成的 jar 文件
ls -la target/

# 运行生成的程序
java -cp target/maven-test-project-1.0-SNAPSHOT.jar com.example.test.App
```

### 多用户配置

#### 为所有用户配置 Maven
```bash
# 确保环境变量对所有用户生效
sudo nano /etc/profile

# 添加内容：
export M2_HOME=/opt/maven/latest
export M2=$M2_HOME/bin
export MAVEN_HOME=/opt/maven/latest
export PATH=$M2:$PATH

# 确保所有用户都能访问 Maven
sudo chmod -R 755 /opt/maven/
```

#### 用户级配置（可选）
```bash
# 如果只为当前用户配置
echo 'export M2_HOME=/opt/maven/latest' >> ~/.bashrc
echo 'export M2=$M2_HOME/bin' >> ~/.bashrc
echo 'export MAVEN_HOME=/opt/maven/latest' >> ~/.bashrc
echo 'export PATH=$M2:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 故障排除

#### 问题1：磁盘空间不足错误

如果遇到类似以下错误：
```
installing package maven-1:3.5.4-5.module_el8.0.0+39+6a9b6e22.noarch needs 65MB on the / filesystem
错误汇总：磁盘需求：在文件系统/上至少需要65MB的可用空间。
```

##### 1.1 检查磁盘空间使用情况
```bash
# 查看磁盘使用情况
df -h

# 示例输出分析：
# /dev/vda1  40G   40G  150M  100% /
# 说明：40GB 硬盘已满，只剩 150MB 可用空间，使用率 100%

# 查看根目录下各目录的大小
du -sh /*

# 查看当前目录下文件大小排序
du -sh * | sort -hr

# 查看隐藏文件的大小
du -sh .[^.]* 2>/dev/null | sort -hr
```

##### 🚨 紧急清理方案（磁盘使用率100%）

**立即执行的清理命令（按优先级）：**

```bash
# 1. 首先清理 Docker 相关（从您的挂载点看有 Docker 容器）
sudo docker system prune -a --volumes -f

# 2. 清理包管理器缓存
sudo yum clean all
sudo rm -rf /var/cache/yum/*

# 3. 清理系统日志
sudo journalctl --vacuum-time=1d
sudo journalctl --vacuum-size=100M

# 4. 清理临时文件
sudo find /tmp -type f -delete 2>/dev/null
sudo find /var/tmp -type f -delete 2>/dev/null

# 5. 清理旧日志文件
sudo find /var/log -name "*.log.*" -type f -delete
sudo find /var/log -name "*.[0-9]" -type f -delete

# 6. 清空大的日志文件（不删除文件本身）
sudo truncate -s 0 /var/log/messages
sudo truncate -s 0 /var/log/secure
sudo truncate -s 0 /var/log/maillog
sudo truncate -s 0 /var/log/cron
```

**一键紧急清理脚本：**
```bash
sudo sh -c '
echo "=== 紧急清理开始 ==="
echo "清理前磁盘使用情况："
df -h /
echo ""

echo "1. 清理 Docker..."
docker system prune -a --volumes -f 2>/dev/null

echo "2. 清理 yum 缓存..."
yum clean all
rm -rf /var/cache/yum/*

echo "3. 清理系统日志..."
journalctl --vacuum-time=1d
journalctl --vacuum-size=50M

echo "4. 清理临时文件..."
find /tmp -type f -atime +3 -delete 2>/dev/null
find /var/tmp -type f -atime +7 -delete 2>/dev/null

echo "5. 清理旧日志..."
find /var/log -name "*.log" -type f -mtime +3 -delete
find /var/log -name "*.log.*" -type f -mtime +7 -delete

echo "6. 清空大日志文件..."
> /var/log/messages
> /var/log/secure  
> /var/log/maillog
> /var/log/cron

echo ""
echo "=== 清理完成 ==="
echo "清理后磁盘使用情况："
df -h /
'
```

##### 1.2 常见的磁盘空间清理方法

**清理系统日志文件：**
```bash
# 查看日志文件大小
sudo du -sh /var/log/*

# 清理系统日志（保留最近7天）
sudo journalctl --vacuum-time=7d

# 清理旧的日志文件
sudo find /var/log -name "*.log" -type f -mtime +3 -delete
sudo find /var/log -name "*.log.*" -type f -mtime +7 -delete

# 清理 wtmp 和 btmp 日志
sudo > /var/log/wtmp
sudo > /var/log/btmp
```

**清理包管理器缓存：**
```bash
# 清理 yum 缓存
sudo yum clean all

# 清理 dnf 缓存（如果使用 dnf）
sudo dnf clean all

# 删除孤立的包
sudo package-cleanup --leaves
sudo package-cleanup --orphans
```

**清理临时文件：**
```bash
# 清理 /tmp 目录
sudo find /tmp -type f -atime +7 -delete
sudo find /tmp -type d -empty -delete

# 清理用户临时文件
sudo find /var/tmp -type f -atime +30 -delete

# 清理核心转储文件
sudo find / -name "core.*" -type f -delete 2>/dev/null
```

**清理旧的内核文件：**
```bash
# 查看已安装的内核版本
rpm -q kernel

# 删除旧内核（保留当前和最新的）
sudo package-cleanup --oldkernels --count=2

# 或者手动删除（谨慎操作）
# sudo yum remove kernel-<old-version>
```

##### 1.3 快速释放空间的命令组合
```bash
# 一键清理脚本
sudo sh -c '
echo "=== 清理开始 ==="
df -h /
echo "清理 yum 缓存..."
yum clean all
echo "清理日志文件..."
journalctl --vacuum-time=3d
find /var/log -name "*.log.*" -type f -mtime +3 -delete
find /var/log -name "*.[0-9]" -type f -delete
echo "清理临时文件..."
find /tmp -type f -atime +3 -delete 2>/dev/null
find /var/tmp -type f -atime +7 -delete 2>/dev/null
echo "=== 清理完成 ==="
df -h /
'
```

##### 1.4 检查大文件和目录
```bash
# 查找最大的文件（大于100MB）
sudo find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null | head -20

# 查找最大的目录
sudo du -h / 2>/dev/null | grep "^[0-9\.]*G" | sort -hr

# 查看根目录下各分区使用情况
sudo du -h --max-depth=1 / 2>/dev/null | sort -hr

# 查看根目录下所有文件夹的空间占用情况（推荐）
sudo du -sh /* 2>/dev/null | sort -hr

# 查看根目录下所有文件夹大小（包括隐藏目录）
sudo du -sh /{*,.[^.]*} 2>/dev/null | sort -hr

# 更详细的根目录分析
sudo du -h --max-depth=1 / 2>/dev/null | grep -E "^[0-9]+[KMG]" | sort -hr

# 只显示大于1GB的目录
sudo du -sh /* 2>/dev/null | grep -E "^[0-9]+G" | sort -hr

# 查看根目录下每个目录的总大小（不递归）
ls -la / | grep "^d" | awk '{print $9}' | xargs -I {} sudo du -sh /{} 2>/dev/null

# 一键查看根目录空间分布脚本
sudo sh -c '
echo "=== 根目录空间分析 ==="
echo "磁盘总使用情况:"
df -h /
echo ""
echo "根目录下各文件夹大小排序:"
du -sh /* 2>/dev/null | sort -hr
echo ""
echo "大于500MB的目录:"
du -sh /* 2>/dev/null | grep -E "^[0-9]+[GM]" | sort -hr
echo ""
echo "所有目录大小（包括小目录）:"
du -sh /* 2>/dev/null | sort -hr
'

# 专门查看 /data 目录具体大小
sudo du -sh /data

# 查看 /data 目录详细内容
sudo du -h --max-depth=1 /data | sort -hr
```

##### 1.6 Docker overlay2 多挂载点解释

**为什么 df -h 显示多个 overlay2 挂载点？**

从您的输出可以看到：
```
overlay  40G   38G  2.4G   95% /var/lib/docker/overlay2/8c3bf20b4b28b7f2b05d11c2c843e4a4d787b45a44646bb90742e774c13c6340/merged
overlay  40G   38G  2.4G   95% /var/lib/docker/overlay2/e61f712edb9c7693ea397ffb1d761276b8e8a8efd2ee14e98ab796c63f6db611/merged
```

**原理解释：**

1. **每个运行的容器都会创建一个 overlay2 挂载点**
   - 每行代表一个正在运行的 Docker 容器
   - overlay2 是 Docker 的存储驱动，用于分层文件系统
   - `merged` 目录是容器的统一视图，包含所有层的内容

2. **overlay2 文件系统结构：**
   ```
   /var/lib/docker/overlay2/<容器ID>/
   ├── diff/     # 容器写入层（可写）
   ├── lower     # 指向基础镜像层（只读）
   ├── upper     # 指向容器写入层
   ├── work/     # overlay2 工作目录
   └── merged/   # 统一挂载点（容器看到的完整文件系统）
   ```

**🔍 查看 Docker 容器与 overlay2 目录的对应关系：**

```bash
# 1. 查看当前运行的容器
docker ps -a

# 2. 查看容器详细信息，找到对应的 overlay2 目录
docker inspect <容器ID或名称> | grep MergedDir

# 3. 查看所有容器的 overlay2 目录
docker ps -q | xargs docker inspect --format='{{.Name}} {{.GraphDriver.Data.MergedDir}}'

# 4. 查看特定容器的存储信息
docker inspect <容器ID> --format='{{json .GraphDriver.Data}}' | jq

# 5. 一键查看所有容器与 overlay2 对应关系
sudo sh -c '
echo "=== Docker 容器与 overlay2 目录对应关系 ==="
echo "运行中的容器:"
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
echo ""
echo "容器与存储目录对应:"
docker ps -q | while read container_id; do
    name=$(docker inspect $container_id --format="{{.Name}}" | sed "s/\///")
    merged_dir=$(docker inspect $container_id --format="{{.GraphDriver.Data.MergedDir}}")
    echo "容器: $name"
    echo "目录: $merged_dir"
    echo "大小: $(du -sh $merged_dir 2>/dev/null | cut -f1)"
    echo "---"
done
'
```

**📊 Docker 存储空间分析：**

```bash
# 1. 查看 Docker 系统整体空间使用
docker system df

# 2. 查看详细的空间使用情况
docker system df -v

# 3. 查看所有 overlay2 目录大小
sudo du -sh /var/lib/docker/overlay2/* | sort -hr | head -20

# 4. 查看 Docker 根目录总大小
sudo du -sh /var/lib/docker

# 5. 分别查看各个组件的空间占用
sudo du -sh /var/lib/docker/containers    # 容器数据
sudo du -sh /var/lib/docker/image         # 镜像数据  
sudo du -sh /var/lib/docker/volumes       # 数据卷
sudo du -sh /var/lib/docker/overlay2      # overlay2 存储
sudo du -sh /var/lib/docker/buildkit      # 构建缓存

# 6. 查看每个容器的实际大小
docker ps -s

# 7. 一键分析 Docker 空间分布
sudo sh -c '
echo "=== Docker 存储空间详细分析 ==="
echo "Docker 系统空间概览:"
docker system df
echo ""
echo "Docker 根目录大小:"
du -sh /var/lib/docker
echo ""
echo "各组件空间占用:"
echo "容器数据: $(du -sh /var/lib/docker/containers 2>/dev/null | cut -f1)"
echo "镜像数据: $(du -sh /var/lib/docker/image 2>/dev/null | cut -f1)" 
echo "数据卷: $(du -sh /var/lib/docker/volumes 2>/dev/null | cut -f1)"
echo "overlay2: $(du -sh /var/lib/docker/overlay2 2>/dev/null | cut -f1)"
echo "构建缓存: $(du -sh /var/lib/docker/buildkit 2>/dev/null | cut -f1)"
echo ""
echo "最大的 overlay2 
du -sh /var/lib/docker/overlay2/* 2>/dev/null | sort -hr | head -10
'
```

**🧹 Docker 空间清理命令：**

```bash
# 1. 清理未使用的资源（安全）
docker system prune

# 2. 清理所有未使用的资源（包括未使用的镜像）
docker system prune -a

# 3. 清理所有资源（包括数据卷，谨慎使用）
docker system prune -a --volumes

# 4. 分别清理各类资源
docker container prune    # 清理停止的容器
docker image prune        # 清理悬空镜像
docker image prune -a     # 清理所有未使用镜像
docker volume prune       # 清理未使用的数据卷
docker network prune      # 清理未使用的网络

# 5. 强制清理（立即释放空间）
docker system prune -a --volumes -f

# 6. 清理构建缓存
docker builder prune
docker builder prune -a   # 清理所有构建缓存

# 7. 查看并删除大容器/镜像
# 查看镜像大小排序
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | sort -k3 -hr

# 删除特定大镜像
# docker rmi <镜像ID>

# 8. 停止并删除所有容器（谨慎使用）
# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)
```

**🚀 Docker 空间清理脚本（适合您当前95%磁盘使用率）：**

```bash
sudo sh -c '
echo "=== Docker 紧急空间清理 ==="
echo "清理前 Docker 空间使用:"
docker system df
echo ""
echo "清理前磁盘空间:"
df -h /
echo ""

echo "1. 清理停止的容器..."
docker container prune -f

echo "2. 清理悬空镜像..."
docker image prune -f

echo "3. 清理未使用的镜像..."
docker image prune -a -f

echo "4. 清理未使用的数据卷..."
docker volume prune -f

echo "5.
docker builder prune -a -f

echo "6. 清理网络..."
docker network prune -f

echo ""
echo "=== 清理完成 ==="
echo "清理后 Docker 空间使用:"
docker system df
echo ""
echo "清理后磁盘空间:"
df -h /
'
```

#### 2. 自动化监控与告警脚本

##### 2.1 磁盘空间监控脚本

**创建磁盘空间监控脚本：**

```bash
# 创建监控脚本目录
sudo mkdir -p /opt/scripts/monitoring

# 创建磁盘空间监控脚本
sudo nano /opt/scripts/monitoring/disk_monitor.sh
```

**磁盘空间监控脚本内容：**

```bash
#!/bin/bash

# 磁盘空间监控与自动清理脚本
# 作者：系统管理员
# 用途：监控磁盘空间，当使用率超过阈值时自动清理并发送告警

# ================================
# 配置参数
# ================================
WARNING_THRESHOLD=80    # 警告阈值（百分比）
CRITICAL_THRESHOLD=90   # 严重阈值（百分比）
EMERGENCY_THRESHOLD=95  # 紧急阈值（百分比）
LOG_FILE="/var/log/disk_monitor.log"
EMAIL_ALERT=""          # 邮箱地址（可选）

# ================================
# 颜色定义
# ================================
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# ================================
# 日志函数
# ================================
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ================================
# 获取磁盘使用率
# ================================
get_disk_usage() {
    df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
}

# ================================
# 发送邮件告警（可选）
# ================================
send_email_alert() {
    local subject="$1"
    local message="$2"
    
    if [ -n "$EMAIL_ALERT" ]; then
        echo "$message" | mail -s "$subject" "$EMAIL_ALERT"
    fi
}

# ================================
# 自动清理函数
# ================================
auto_cleanup() {
    local cleanup_level=$1
    
    log_message "开始执行清理级别: $cleanup_level"
    
    case $cleanup_level in
        "basic")
            log_message "执行基础清理..."
            # 清理系统日志
            sudo journalctl --vacuum-time=7d
            # 清理包管理器缓存
            sudo yum clean all
            # 清理临时文件
            sudo find /tmp -type f -atime +7 -delete
            ;;
            
        "medium")
            log_message "执行中级清理..."
            # 执行基础清理
            auto_cleanup "basic"
            # 清理 Docker
            docker system prune -f
            # 清理旧内核
            package-cleanup --oldkernels --count=1 -y 2>/dev/null || true
            ;;
            
        "aggressive")
            log_message "执行激进清理..."
            # 执行中级清理
            auto_cleanup "medium"
            # 清理所有 Docker 资源
            docker system prune -a -f
            # 清理更多临时文件
            sudo find /var/tmp -type f -atime +3 -delete
            sudo find /var/log -name "*.old" -delete
            sudo find /var/log -name "*.gz" -mtime +30 -delete
            ;;
    esac
    
    log_message "清理完成，当前磁盘使用率: $(get_disk_usage)%"
}

# ================================
# 主监控逻辑
# ================================
main() {
    local current_usage=$(get_disk_usage)
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    log_message "磁盘使用率检查: ${current_usage}%"
    
    if [ "$current_usage" -ge "$EMERGENCY_THRESHOLD" ]; then
        echo -e "${RED}🚨 紧急告警：磁盘使用率 ${current_usage}% 超过紧急阈值 ${EMERGENCY_THRESHOLD}%${NC}"
        log_message "紧急告警：磁盘使用率 ${current_usage}% 超过紧急阈值"
        auto_cleanup "aggressive"
        send_email_alert "紧急：服务器磁盘空间不足" "服务器磁盘使用率达到 ${current_usage}%，已执行激进清理"
        
    elif [ "$current_usage" -ge "$CRITICAL_THRESHOLD" ]; then
        echo -e "${YELLOW}⚠️  严重告警：磁盘使用率 ${current_usage}% 超过严重阈值 ${CRITICAL_THRESHOLD}%${NC}"
        log_message "严重告警：磁盘使用率 ${current_usage}% 超过严重阈值"
        auto_cleanup "medium"
        send_email_alert "警告：服务器磁盘空间紧张" "服务器磁盘使用率达到 ${current_usage}%，已执行中级清理"
        
    elif [ "$current_usage" -ge "$WARNING_THRESHOLD" ]; then
        echo -e "${YELLOW}⚠️  警告：磁盘使用率 ${current_usage}% 超过警告阈值 ${WARNING_THRESHOLD}%${NC}"
        log_message "警告：磁盘使用率 ${current_usage}% 超过警告阈值"
        auto_cleanup "basic"
        send_email_alert "提醒：服务器磁盘空间预警" "服务器磁盘使用率达到 ${current_usage}%，已执行基础清理"
        
    else
        echo -e "${GREEN}✅ 正常：磁盘使用率 ${current_usage}%${NC}"
    fi
    
    # 显示当前磁盘状态
    echo ""
    echo "当前磁盘状态："
    df -h /
    echo ""
    echo "Docker 空间使用："
    docker system df 2>/dev/null || echo "Docker 未运行或不可用"
}

# ================================
# 脚本入口
# ================================
if [ "$#" -eq 0 ]; then
    main
else
    case "$1" in
        "check")
            main
            ;;
        "cleanup")
            auto_cleanup "${2:-basic}"
            ;;
        "test")
            echo "测试模式："
            echo "当前磁盘使用率: $(get_disk_usage)%"
            echo "警告阈值: $WARNING_THRESHOLD%"
            echo "严重阈值: $CRITICAL_THRESHOLD%"
            echo "紧急阈值: $EMERGENCY_THRESHOLD%"
            ;;
        *)
            echo "用法: $0 [check|cleanup [basic|medium|aggressive]|test]"
            exit 1
            ;;
    esac
fi
```

##### 2.2 系统资源监控脚本

**创建系统资源监控脚本：**

```bash
sudo nano /opt/scripts/monitoring/system_monitor.sh
```

**系统资源监控脚本内容：**

```bash
#!/bin/bash

# 系统资源全面监控脚本
# 监控：CPU、内存、磁盘、网络、进程等

# ================================
# 配置参数
# ================================
LOG_FILE="/var/log/system_monitor.log"
REPORT_FILE="/var/log/system_report_$(date +%Y%m%d).log"

# ================================
# 颜色定义
# ================================
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# ================================
# 生成系统报告
# ================================
generate_report() {
    echo "========================================" > "$REPORT_FILE"
    echo "系统监控报告 - $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
    echo "========================================" >> "$REPORT_FILE"
    
    # 系统基本信息
    echo "" >> "$REPORT_FILE"
    echo "=== 系统信息 ===" >> "$REPORT_FILE"
    echo "主机名: $(hostname)" >> "$REPORT_FILE"
    echo "系统版本: $(cat /etc/centos-release 2>/dev/null || cat /etc/redhat-release)" >> "$REPORT_FILE"
    echo "内核版本: $(uname -r)" >> "$REPORT_FILE"
    echo "系统运行时间: $(uptime)" >> "$REPORT_FILE"
    
    # CPU 信息
    echo "" >> "$REPORT_FILE"
    echo "=== CPU 使用率 ===" >> "$REPORT_FILE"
    top -bn1 | grep "Cpu(s)" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "CPU 详细信息:" >> "$REPORT_FILE"
    cat /proc/cpuinfo | grep "model name" | head -1 >> "$REPORT_FILE"
    echo "CPU 核心数: $(nproc)" >> "$REPORT_FILE"
    
    # 内存信息
    echo "" >> "$REPORT_FILE"
    echo "=== 内存使用情况 ===" >> "$REPORT_FILE"
    free -h >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "内存使用率: $(free | grep Mem | awk '{printf "%.2f%%", $3/$2 * 100.0}')" >> "$REPORT_FILE"
    
    # 磁盘信息
    echo "" >> "$REPORT_FILE"
    echo "=== 磁盘使用情况 ===" >> "$REPORT_FILE"
    df -h >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "磁盘 I/O 状态:" >> "$REPORT_FILE"
    iostat -x 1 1 2>/dev/null >> "$REPORT_FILE" || echo "iostat 不可用" >> "$REPORT_FILE"
    
    # 网络信息
    echo "" >> "$REPORT_FILE"
    echo "=== 网络连接情况 ===" >> "$REPORT_FILE"
    netstat -tuln | head -20 >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "网络接口流量:" >> "$REPORT_FILE"
    cat /proc/net/dev | head -10 >> "$REPORT_FILE"
    
    # 进程信息
    echo "" >> "$REPORT_FILE"
    echo "=== 资源占用 TOP 10 进程 ===" >> "$REPORT_FILE"
    echo "CPU 占用最高的进程:" >> "$REPORT_FILE"
    ps aux --sort=-%cpu | head -11 >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "内存占用最高的进程:" >> "$REPORT_FILE"
    ps aux --sort=-%mem | head -11 >> "$REPORT_FILE"
    
    # Docker 信息（如果可用）
    if command -v docker > /dev/null 2>&1; then
        echo "" >> "$REPORT_FILE"
        echo "=== Docker 状态 ===" >> "$REPORT_FILE"
        docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "Docker 空间使用:" >> "$REPORT_FILE"
        docker system df >> "$REPORT_FILE"
    fi
    
    # 系统日志错误
    echo "" >> "$REPORT_FILE"
    echo "=== 最近系统错误 ===" >> "$REPORT_FILE"
    journalctl --since "1 hour ago" --priority=err -n 10 >> "$REPORT_FILE"
    
    echo "" >> "$REPORT_FILE"
    echo "========================================" >> "$REPORT_FILE"
    echo "报告生成完成 - $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
    echo "========================================" >> "$REPORT_FILE"
}

# ================================
# 实时监控显示
# ================================
show_realtime_monitor() {
    clear
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}         系统实时监控面板${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # 系统基本信息
    echo -e "\n${GREEN}=== 系统信息 ===${NC}"
    echo "主机名: $(hostname)"
    echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "系统运行时间: $(uptime | awk -F'load' '{print $1}' | sed 's/^.*up //')"
    
    # CPU 和负载
    echo -e "\n${GREEN}=== CPU 和负载 ===${NC}"
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')
    load_avg=$(uptime | awk -F'load average:' '{print $2}')
    echo "CPU 使用率: ${cpu_usage}%"
    echo "负载平均值:${load_avg}"
    
    # 内存使用
    echo -e "\n${GREEN}=== 内存使用 ===${NC}"
    mem_info=$(free -h | grep Mem)
    mem_total=$(echo $mem_info | awk '{print $2}')
    mem_used=$(echo $mem_info | awk '{print $3}')
    mem_percent=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
    echo "内存总量: $mem_total"
    echo "已用内存: $mem_used ($mem_percent%)"
    
    # 磁盘使用
    echo -e "\n${GREEN}=== 磁盘使用 ===${NC}"
    disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    disk_avail=$(df -h / | awk 'NR==2 {print $4}')
    echo "根分区使用率: ${disk_usage}%"
    echo "可用空间: $disk_avail"
    
    if [ "$disk_usage" -ge 90 ]; then
        echo -e "${RED}⚠️  磁盘空间严重不足！${NC}"
    elif [ "$disk_usage" -ge 80 ]; then
        echo -e "${YELLOW}⚠️  磁盘空间不足警告${NC}"
    fi
    
    # Docker 状态
    if command -v docker > /dev/null 2>&1; then
        echo -e "\n${GREEN}=== Docker 状态 ===${NC}"
        container_count=$(docker ps -q | wc -l)
        echo "运行中容器: $container_count"
        if [ "$container_count" -gt 0 ]; then
            docker ps --format "table {{.Names}}\t{{.Status}}"
        fi
    fi
    
    # 网络连接
    echo -e "\n${GREEN}=== 网络连接 ===${NC}"
    established_conn=$(netstat -an | grep ESTABLISHED | wc -l)
    listening_ports=$(netstat -tuln | grep LISTEN | wc -l)
    echo "活跃连接数: $established_conn"
    echo "监听端口数: $listening_ports"
    
    echo -e "\n${BLUE}========================================${NC}"
    echo "按 Ctrl+C 退出监控"
}

# ================================
# 主函数
# ================================
main() {
    case "${1:-monitor}" in
        "report")
            echo "生成系统报告..."
            generate_report
            echo "报告已保存到: $REPORT_FILE"
            ;;
        "monitor")
            while true; do
                show_realtime_monitor
                sleep 5
            done
            ;;
        "check")
            generate_report
            cat "$REPORT_FILE"
            ;;
        *)
            echo "用法: $0 [monitor|report|check]"
            echo "  monitor  - 实时监控面板（默认）"
            echo "  report   - 生成详细报告"
            echo "  check    - 检查并显示报告"
            exit 1
            ;;
    esac
}

main "$@"
```

#### 邮件队列堆积问题解决

### 问题现象
- `/var/spool/postfix` 占用大量空间（如18G）
- `mailq` 显示大量未发送邮件
- 通常由 Cron 任务产生的邮件堆积

### 排查步骤
```bash
# 1. 检查磁盘使用
sudo du -sh /var/spool/* | sort -hr

# 2. 查看邮件队列
mailq

# 3. 查看具体邮件内容
sudo postcat -q [邮件ID]

# 4. 检查 Cron 任务
crontab -l
```

### 常见原因
1. **Cron 任务输出重定向错误**
   - `/dev/nul` 拼写错误，应为 `/dev/null`
   - 导致 curl 进度信息输出，Cron 自动发邮件

2. **Postfix 配置问题**
   - 邮件无法正确投递到本地
   - 域名解析失败

### 解决方案

#### 1. 修复 Cron 任务
```bash
# 编辑 crontab
crontab -e

# 修改错误的重定向
# 原来：curl https://example.com -o /dev/nul  
# 修改为：curl -s https://example.com > /dev/null 2>&1

# 或禁用邮件通知
MAILTO=""
```

#### 2. 配置 Postfix 本地投递
```bash
# 修改配置
sudo postconf -e "inet_interfaces = localhost"
sudo postconf -e "mydomain = localdomain"
sudo postconf -e "mydestination = \$myhostname, localhost.\$mydomain, localhost"

# 重启服务
sudo systemctl restart postfix
```

#### 3. 清空邮件队列
```bash
# 停止服务
sudo systemctl stop postfix

# 清空所有邮件
sudo postsuper -d ALL

# 重启服务
sudo systemctl start postfix
```

#### 4. 预防措施
```bash
# 定期清理队列
echo "0 2 * * 0 root postsuper -d ALL" | sudo tee -a /etc/crontab

# 或禁用邮件服务（如不需要）
sudo systemctl disable postfix
```

### 验证修复
```bash
# 测试本地邮件投递
echo "test" | mail root
sudo mail -u root

# 监控队列大小
watch "mailq | tail -1"
```

### 实际案例解决过程

#### 问题配置检查结果
经过检查，Postfix 配置是正确的：
```bash
inet_interfaces = localhost
mydestination = $myhostname, localhost.$mydomain, localhost
mydomain = localdomain
myhostname = iZbp19x33g3xalajeui4mzZ.localdomain
```

#### 根本原因确认
问题出在 Cron 任务的拼写错误：
```bash
# 错误的 crontab 配置
* * * * * curl https://camp.hilazyfish.com/ping -o /dev/nul  
* * * * * curl https://camp.hilazyfish.com/panic -o /dev/nul  
* * * * * curl https://camp.hilazyfish.com/hello -o /dev/nul
```

#### 解决步骤
1. **立即清空邮件队列**：
```bash
sudo systemctl stop postfix
sudo postsuper -d ALL
sudo systemctl start postfix
```

2. **修复 Cron 任务**：
```bash
crontab -e
# 修改为：
MAILTO=""
* * * * * curl -s https://camp.hilazyfish.com/ping > /dev/null 2>&1
* * * * * curl -s https://camp.hilazyfish.com/panic > /dev/null 2>&1
* * * * * curl -s https://camp.hilazyfish.com/hello > /dev/null 2>&1
```

3. **验证修复**：
```bash
# 检查磁盘空间
df -h /var/spool/postfix

# 监控新邮件生成
watch "mailq | tail -1"

# 等待几分钟确认不再产生新邮件
```

#### 预防措施
```bash
# 添加磁盘空间监控
echo "0 */6 * * * [ \$(df / | tail -1 | awk '{print \$5}' | sed 's/%//') -gt 85 ] && echo 'Disk usage high' | logger" | crontab -

# 定期清理邮件队列
echo "0 2 * * 0 postsuper -d ALL" | sudo tee -a /etc/crontab
```

## 安装Conda（Miniconda/Anaconda）

### 前提条件
确保系统已更新并具备基本开发工具：
```bash
# 更新系统
sudo yum update -y

# 安装必要工具
sudo yum install -y wget curl bzip2
```

### 方法一：安装Miniconda（推荐，轻量级）

#### 1.1 下载Miniconda
```bash
# 创建安装目录
mkdir -p ~/downloads
cd ~/downloads

# 下载最新版本的Miniconda（Python 3.11版本）
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 或使用清华大学镜像（国内用户推荐）
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 验证下载完整性（可选）
sha256sum Miniconda3-latest-Linux-x86_64.sh
```

#### 1.2 安装Miniconda
```bash
# 给安装脚本添加执行权限
chmod +x Miniconda3-latest-Linux-x86_64.sh

# 运行安装脚本
bash Miniconda3-latest-Linux-x86_64.sh

# 安装过程中的选择：
# 1. 阅读许可协议后输入 yes
# 2. 确认安装路径（默认：/home/用户名/miniconda3）
# 3. 询问是否初始化conda时选择 yes
```

#### 1.3 配置环境变量
```bash
# 如果安装时没有选择自动初始化，手动添加到环境变量
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc

# 重新加载bash配置
source ~/.bashrc

# 或者直接初始化conda
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

### 方法二：安装完整版Anaconda

#### 2.1 下载Anaconda
```bash
cd ~/downloads

# 下载Anaconda（包含更多预装包，文件较大约500MB+）
wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh

# 或使用清华镜像
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
```

#### 2.2 安装Anaconda
```bash
chmod +x Anaconda3-2023.09-0-Linux-x86_64.sh
bash Anaconda3-2023.09-0-Linux-x86_64.sh

# 按照提示完成安装
# 默认安装路径：/home/用户名/anaconda3
```

### 验证安装

#### 3.1 检查conda版本
```bash
# 检查conda版本
conda --version

# 检查conda信息
conda info

# 列出已安装的包
conda list

# 检查Python版本
python --version
```

#### 3.2 测试conda功能
```bash
# 查看可用的conda环境
conda env list

# 创建测试环境
conda create -n test_env python=3.9

# 激活测试环境
conda activate test_env

# 在测试环境中安装包
conda install numpy pandas

# 退出环境
conda deactivate

# 删除测试环境
conda remove -n test_env --all
```

### 配置Conda

#### 4.1 配置国内镜像源（提高下载速度）
```bash
# 添加清华大学镜像源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2/

# 添加conda-forge镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/

# 设置搜索时显示通道地址
conda config --set show_channel_urls yes

# 查看配置
conda config --show channels
```

#### 4.2 创建conda配置文件
```bash
# 创建或编辑.condarc配置文件
nano ~/.condarc

# 添加以下内容：
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
  - defaults

show_channel_urls: true
ssl_verify: true
auto_activate_base: false  # 防止每次启动终端自动激活base环境

# 保存文件并退出
```

#### 4.3 禁用自动激活base环境（可选）
```bash
# 禁用conda自动激活base环境
conda config --set auto_activate_base false

# 如果需要重新启用
# conda config --set auto_activate_base true
```

### Conda常用命令

#### 5.1 环境管理
```bash
# 创建新环境
conda create -n myenv python=3.9

# 创建环境并安装包
conda create -n myenv python=3.9 numpy pandas matplotlib

# 从文件创建环境
conda env create -f environment.yml

# 激活环境
conda activate myenv

# 退出环境
conda deactivate

# 列出所有环境
conda env list
conda info --envs

# 删除环境
conda remove -n myenv --all

# 克隆环境
conda create -n newenv --clone myenv
```

#### 5.2 包管理
```bash
# 搜索包
conda search package_name

# 安装包
conda install package_name
conda install package_name=1.4.3  # 指定版本

# 从指定频道安装
conda install -c conda-forge package_name

# 更新包
conda update package_name
conda update --all  # 更新所有包

# 卸载包
conda remove package_name

# 列出已安装包
conda list
conda list package_name  # 查看特定包

# 导出环境配置
conda env export > environment.yml

# 从配置文件安装环境
conda env create -f environment.yml
```

#### 5.3 conda自身管理
```bash
# 更新conda
conda update conda

# 更新anaconda
conda update anaconda

# 清理缓存
conda clean --all
conda clean --packages  # 清理包缓存
conda clean --tarballs   # 清理压缩包缓存

# 查看conda配置
conda config --show

# 重置conda配置
conda config --remove-key channels
```

### 多用户安装配置

#### 6.1 系统级安装（所有用户可用）
```bash
# 安装到系统目录
sudo mkdir -p /opt/miniconda3

# 下载并安装到系统目录
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sudo bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3

# 设置权限
sudo chown -R root:root /opt/miniconda3
sudo chmod -R 755 /opt/miniconda3

# 为所有用户配置环境变量
sudo nano /etc/profile.d/conda.sh

# 添加内容：
#!/bin/bash
export PATH="/opt/miniconda3/bin:$PATH"

# 设置可执行权限
sudo chmod +x /etc/profile.d/conda.sh

# 重新加载环境变量
source /etc/profile.d/conda.sh
```

#### 6.2 用户级配置
```bash
# 每个用户初始化conda
/opt/miniconda3/bin/conda init bash

# 或手动添加到用户的.bashrc
echo 'export PATH="/opt/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 故障排除

#### 7.1 常见问题解决

**问题1：conda命令找不到**
```bash
# 解决方案：检查PATH环境变量
echo $PATH | grep conda

# 如果没有，重新添加
export PATH="$HOME/miniconda3/bin:$PATH"
source ~/.bashrc
```

**问题2：权限不足**
```bash
# 检查conda目录权限
ls -la ~/miniconda3/

# 修复权限
chmod -R 755 ~/miniconda3/
```

**问题3：下载速度慢**
```bash
# 使用国内镜像重新配置
conda config --remove-key channels
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
```

**问题4：SSL证书错误**
```bash
# 临时禁用SSL验证（不推荐在生产环境）
conda config --set ssl_verify false

# 更好的解决方案：更新证书
conda update ca-certificates
```

#### 7.2 完全卸载conda
```bash
# 删除conda目录
rm -rf ~/miniconda3
# 或
rm -rf ~/anaconda3

# 清理环境变量
nano ~/.bashrc
# 删除conda相关的export语句

# 清理配置文件
rm -rf ~/.conda
rm -f ~/.condarc

# 重新加载bash
source ~/.bashrc
```

### 性能优化

#### 8.1 conda性能优化
```bash
# 启用libmamba求解器（更快的依赖解析）
conda install -n base conda-libmamba-solver
conda config --set solver libmamba

# 禁用不必要的插件
conda config --set pip_interop_enabled false
```

#### 8.2 磁盘空间管理
```bash
# 定期清理conda缓存
conda clean --all

# 查看缓存大小
du -sh ~/.conda/pkgs

# 配置包缓存位置
conda config --add pkgs_dirs /path/to/custom/cache
```

### 安全考虑

#### 9.1 验证安装包完整性
```bash
# 安装前验证校验和
sha256sum Miniconda3-latest-Linux-x86_64.sh

# 使用官方源
conda config --set channel_priority strict
```

#### 9.2 环境隔离最佳实践
```bash
# 为每个项目创建独立环境
conda create -n project1 python=3.9
conda create -n project2 python=3.8

# 导出环境配置用于版本控制
conda env export --no-builds > environment.yml
```

### 示例：创建数据科学环境

```bash
# 创建数据科学工作环境
conda create -n datascience python=3.9

# 激活环境
conda activate datascience

# 安装常用数据科学包
conda install numpy pandas matplotlib seaborn scikit-learn jupyter notebook

# 或一次性安装
conda create -n datascience python=3.9 numpy pandas matplotlib seaborn scikit-learn jupyter notebook

# 启动Jupyter Notebook
jupyter notebook

# 退出环境
conda deactivate
```

## Conda CPU占用过高问题分析与解决

### 问题现象
安装conda后可能出现以下情况：
- conda命令执行时CPU使用率飙升到90%+
- conda安装包时系统响应缓慢
- conda环境激活/切换时CPU占用过高
- 后台有conda相关进程持续占用CPU

### 常见原因分析

#### 1. 依赖解析过程（最常见原因）
```bash
# 查看conda解析过程
conda install package_name -v

# conda需要计算复杂的依赖关系，这个过程CPU密集
# 特别是在以下情况下：
# - 安装复杂包（如tensorflow, pytorch）
# - 环境中已有大量包
# - 包版本冲突需要解决
```

#### 2. 求解器性能问题
```bash
# 查看当前使用的求解器
conda config --show solver

# 默认的classic求解器性能较差
# 表现：conda solving environment 阶段耗时很长
```

#### 3. 索引更新和缓存构建
```bash
# conda会定期更新包索引，这是CPU密集型操作
conda search --info package_name  # 会触发索引更新

# 查看缓存目录大小
du -sh ~/.conda/pkgs
```

#### 4. 多进程并发问题
```bash
# 多个conda进程同时运行
ps aux | grep conda

# 可能出现的进程：
# - conda安装进程
# - conda索引更新进程  
# - conda环境解析进程
```

### 解决方案

#### 🚀 方案1：使用高性能求解器（强烈推荐）
```bash
# 安装mamba（C++实现的conda替代品）
conda install mamba -n base -c conda-forge

# 或安装libmamba求解器
conda install -n base conda-libmamba-solver
conda config --set solver libmamba

# 使用mamba替代conda命令（速度提升5-10倍）
mamba install package_name
mamba create -n myenv python=3.9
mamba env create -f environment.yml

# 验证求解器配置
conda config --show solver
```

#### ⚡ 方案2：优化conda配置
```bash
# 1. 禁用不必要的功能
conda config --set pip_interop_enabled false
conda config --set conda_build false

# 2. 限制频道数量（减少索引大小）
conda config --set channel_priority strict
conda config --show channels

# 3. 禁用自动更新
conda config --set auto_update_conda false

# 4. 设置并发限制
conda config --set default_threads 2  # 限制线程数
```

#### 🧹 方案3：清理和优化
```bash
# 1. 清理conda缓存
conda clean --all -y

# 2. 重建索引缓存
conda search --info python  # 强制重建索引

# 3. 清理损坏的缓存
rm -rf ~/.conda/pkgs/cache
conda clean --index-cache

# 4. 压缩索引文件
conda clean --packages
```

#### 🔧 方案4：系统级优化
```bash
# 1. 增加交换内存（如果内存不足）
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 2. 调整进程优先级
nice -n 10 conda install package_name  # 降低优先级

# 3. 监控资源使用
htop  # 实时监控
iotop # 监控磁盘I/O
```

### 一键优化脚本
```bash
#!/bin/bash
echo "=== Conda性能优化开始 ==="

# 1. 检查当前配置
echo "当前conda配置："
conda config --show solver

# 2. 安装高性能求解器
echo "安装libmamba求解器..."
conda install -n base conda-libmamba-solver -y

# 3. 配置libmamba
echo "配置libmamba求解器..."
conda config --set solver libmamba

# 4. 优化配置
echo "优化conda配置..."
conda config --set pip_interop_enabled false
conda config --set auto_update_conda false
conda config --set channel_priority strict

# 5. 清理缓存
echo "清理缓存..."
conda clean --all -y

# 6. 验证配置
echo "优化后配置："
conda config --show solver

echo "=== 优化完成 ==="
```

### 性能监控和诊断

#### 🔍 诊断工具
```bash
# 1. 监控conda进程
watch "ps aux | grep conda | grep -v grep"

# 2. 分析CPU使用
top -p $(pgrep -d',' conda)

# 3. 查看conda详细日志
conda install package_name --debug -v

# 4. 检查系统资源
free -h              # 内存使用
df -h               # 磁盘空间
nproc               # CPU核心数
```

### 最佳实践

#### 🛡️ 推荐做法
```bash
# 1. 使用mamba替代conda（性能提升显著）
conda install mamba -c conda-forge
mamba install package_name

# 2. 创建环境时一次性安装所有包
mamba create -n myenv python=3.9 numpy pandas matplotlib

# 3. 使用环境文件管理依赖
cat > environment.yml << EOF
name: myproject
channels:
  - conda-forge
dependencies:
  - python=3.9
  - numpy
  - pandas
EOF

mamba env create -f environment.yml

# 4. 定期清理维护
conda clean --all
conda update conda
```

#### ⚠️ 避免的操作
```bash
# ❌ 避免这些高CPU操作
conda update --all              # 更新所有包
conda search "*"                # 搜索所有包
conda install pkg1 pkg2 pkg3    # 多包分别安装

# ✅ 推荐的替代方式
mamba update package_name       # 使用mamba
conda search package_name       # 精确搜索
mamba install pkg1 pkg2 pkg3    # 使用mamba批量安装
```

如果按照以上方案优化后仍有问题，建议考虑使用pyenv等轻量级Python版本管理工具替代conda。

## 安装Git，配置Git
```bash
# 安装Git
sudo yum install -y git

# 验证安装
git --version

# 配置用户信息
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# 查看配置
git config --list
```

### 常用Git命令

```bash
# 克隆仓库
git clone https://github.com/user/repo.git

# 查看状态
git status

# 添加文件到暂存区
git add filename

# 提交更改
git commit -m "提交信息"

# 推送到远程仓库
git push origin branch_name

# 拉取远程仓库最新代码
git pull origin branch_name

# 查看日志
git log

# 分支管理
git branch                # 查看所有分支
git branch -b new_branch  # 创建新分支并切换
git checkout -b new_branch # 创建并切换到新分支
git merge branch_name     # 合并分支
git branch -d branch_name # 删除分支
```

### SSH密钥配置（推荐）

```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "you@example.com"

# 启动ssh-agent
eval "$(ssh-agent -s)"

# 添加私钥到ssh-agent
ssh-add ~/.ssh/id_rsa

# 将公钥添加到Git服务（如GitHub、GitLab等）
cat ~/.ssh/id_rsa.pub

# 测试SSH连接
ssh -T git@github.com
```

### 常见问题解决

```bash
# 问题1：权限被拒绝（publickey）
# 解决方案：确保SSH密钥已添加到ssh-agent，并在Git服务中注册

# 问题2：无法推送到远程仓库
# 解决方案：检查远程仓库URL和权限
git remote -v
git remote set-url origin new_url

# 问题3：合并冲突
# 解决方案：手动解决冲突后，添加并提交更改
git add conflicted_file
git commit -m "解决合并冲突"
```

### Git GUI工具

- **GitKraken**：跨平台Git GUI客户端，界面友好，功能强大。
- **Sourcetree**：Atlassian出品的Git和Mercurial桌面客户端，支持Windows和macOS。
- **GitHub Desktop**：GitHub官方的桌面客户端，简化Git操作，适合新手。

### Git工作流建议

- **使用SSH协议**：提高安全性和便利性。
- **定期提交**：保持提交粒度小，便于追踪和回滚。
- **写好提交信息**：清晰描述本次提交的目的和内容。
- **使用分支管理特性**：在新分支上开发新特性，避免影响主分支稳定性。
- **定期同步远程仓库**：保持与远程仓库的同步，减少合并冲突可能性。