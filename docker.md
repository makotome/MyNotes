# Docker

### 在 CentOS 中启动 Docker 服务

#### 1. 安装 Docker（如果未安装）
```bash
# 安装 Docker
sudo yum install -y docker

# 或者安装最新版本的 Docker CE
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
```

#### 2. 启动 Docker 服务
```bash
# 启动 Docker 服务
sudo systemctl start docker

# 设置 Docker 开机自启
sudo systemctl enable docker

# 重启 Docker 服务
sudo systemctl restart docker

# 停止 Docker 服务
sudo systemctl stop docker
```

#### 3. 检查 Docker 状态
```bash
# 查看 Docker 服务状态
sudo systemctl status docker

# 查看 Docker 版本
docker --version

# 测试 Docker 是否正常工作
sudo docker run hello-world
```

#### 4. 添加用户到 docker 组（可选）
```bash
# 将当前用户添加到 docker 组，避免每次使用 sudo
sudo usermod -aG docker $USER

# 重新登录或执行以下命令使组权限生效
newgrp docker

# 测试是否可以不使用 sudo 运行 docker
docker run hello-world
```
