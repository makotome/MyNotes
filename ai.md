## 智普AI开放平台
https://bigmodel.cn/console/overview

## Python SDK 使用

### 1. 安装SDK
```bash
pip install zhipuai
```

### 2. 基础使用示例
```python
from zhipuai import ZhipuAI

# 初始化客户端
client = ZhipuAI(api_key="your_secret_key")

# 发送聊天请求
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]
)

print(response.choices[0].message.content)
```

### 3. 支持的模型
- **glm-4**: 最新通用模型
- **glm-4v**: 多模态模型（支持图像）
- **glm-3-turbo**: 快速轻量模型

### 4. 高级功能
- 流式输出
- 函数调用
- 图像理解
- 多轮对话

详细测试代码请查看：`ZhiPuAI/` 文件夹