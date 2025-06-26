# FunASR & SenseVoiceSmall 使用指南

## 1. 环境安装

```bash
# 安装 FunASR
pip install funasr

# 安装其他依赖
pip install torch torchaudio
pip install modelscope  # 如果需要从 ModelScope 下载模型
```

## 2. SenseVoiceSmall 本地模型使用

### 模型路径配置
- 请将您的本地模型路径修改到代码中的 `model_dir` 变量
- 支持的路径格式：
  - 本地绝对路径：`/path/to/your/SenseVoiceSmall`
  - 本地相对路径：`./models/SenseVoiceSmall`
  - ModelScope 模型ID：`iic/SenseVoiceSmall`（会自动下载）

### 主要功能
1. **语音转文字 (ASR)** - 支持多语言识别
2. **情感识别 (SER)** - 识别说话者情感
3. **音频事件检测 (AED)** - 检测音频事件
4. **语言识别 (LID)** - 识别说话语言

### 支持的语言
- 中文（普通话）
- 粤语
- 英语
- 日语
- 韩语
- 其他 50+ 种语言

## 3. 文件说明

- `basic_demo.py` - 基础使用示例
- `advanced_demo.py` - 高级功能演示
- `batch_processing.py` - 批量处理示例
- `real_time_demo.py` - 实时识别示例
- `emotion_detection.py` - 情感识别专用
- `requirements.txt` - 依赖包列表

## 4. 注意事项

1. **音频格式**：支持任意格式（mp3、wav、flac等）
2. **音频长度**：建议单段音频 ≤ 30秒，长音频会自动分段
3. **设备要求**：推荐使用 GPU 加速，CPU 也可运行
4. **内存需求**：模型较小，内存需求不高

## 5. 常见问题

### 模型路径错误
确保模型路径正确，包含必要的模型文件

### 音频格式不支持
使用 ffmpeg 转换音频格式：
```bash
ffmpeg -i input.xxx -ar 16000 output.wav
```

### 依赖包冲突
建议使用虚拟环境隔离依赖
