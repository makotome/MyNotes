
## 第一步 选好你的项目目录
例如，我规划了我的项目目录是，这是一个新建的空白的目录，如果你不想出错，可以和我一样
```bash
/home/system/xiaozhi
```

## 第二步 克隆本项目
```bash
git clone https://ghproxy.net/https://github.com/makotome/xiaozhi-esp32-server.git
```

## 在Linux下安装libopus
```bash
sudo yum install opus
```

## 在Linux下安装ffmpeg
1. 下载并解压
```bash
# 下载最新静态版本
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

# 解压
tar -xJf ffmpeg-release-amd64-static.tar.xz
cd ffmpeg-*-static
```

2. 复制到系统路径
```bash
# 复制可执行文件到 /usr/local/bin
sudo cp ffmpeg ffprobe /usr/local/bin/
```


## 测试

http://121.40.104.188:8002/xiaozhi/doc.html