# conda 使用常见文

## conda配置文件

```bash
vim ~/.condarc
```

## 恢复默认配置
    * 如果需要恢复默认配置，只需删除 .condarc 文件：
```bash
rm ~/.condarc  # Linux/macOS

# 或者 移除所有自定义通道，恢复为官方默认配置
conda config --remove-key channels 
```

## 添加国内清华镜像()
```yaml
channels:
  - defaults
  - conda-forge
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge
show_channel_urls: true
```
**发现还是使用默认的渠道加代理比较好**

## 查看镜像渠道
```bash
conda config --show channels
```