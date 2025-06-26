# 智谱AI Python SDK 测试指南

## 1. 安装依赖

```bash
pip install zhipuai python-dotenv
```

或者使用项目中的requirements.txt：

```bash
pip install -r requirements.txt
```

## 2. 配置API密钥

### 方法1: 使用环境变量文件（推荐）
1. 编辑 `.env` 文件
2. 将 `your_secret_key_here` 替换为您的实际API密钥

### 方法2: 直接在代码中设置
在 `simple_test.py` 或 `test_zhipuai.py` 中直接修改 `API_KEY` 变量

## 3. 运行测试

### API密钥验证（推荐先运行）
```bash
python verify_api.py
```

### 简单测试
```bash
python simple_test.py
```

### 全面测试
```bash
python test_zhipuai.py
```

## 4. 支持的模型

- **glm-4**: 最新的通用模型，支持文本对话
- **glm-4v**: 支持视觉理解的多模态模型
- **glm-3-turbo**: 更快速的轻量级模型

## 5. 主要功能

### 基础聊天
```python
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your_api_key")
response = client.chat.completions.create(
    model="glm-4",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

### 流式输出
```python
response = client.chat.completions.create(
    model="glm-4",
    messages=[{"role": "user", "content": "写一首诗"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### 函数调用
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"}
            }
        }
    }
}]

response = client.chat.completions.create(
    model="glm-4",
    messages=[{"role": "user", "content": "北京天气怎么样？"}],
    tools=tools
)
```

### 图像理解（glm-4v模型）
```python
messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": "描述这张图片"},
        {"type": "image_url", "image_url": {"url": "图片URL"}}
    ]
}]

response = client.chat.completions.create(
    model="glm-4v",
    messages=messages
)
```

## 6. 错误处理

常见错误及解决方案：

### 401 认证错误（令牌已过期或验证不正确）
```
zhipuai.core._errors.APIAuthenticationError: Error code: 401
```
**解决方案：**
1. 检查 `.env` 文件中的API密钥是否正确
2. 登录 [智谱AI控制台](https://bigmodel.cn/console/overview) 检查密钥状态
3. 如果密钥过期，请重新生成新的密钥
4. 运行 `python verify_api.py` 验证密钥

### 其他常见错误
1. **网络连接问题**: 检查网络连接
2. **模型不存在**: 确认使用的模型名称正确
3. **请求频率限制**: 适当降低请求频率
4. **包导入错误**: 确保已安装 `zhipuai` 和 `python-dotenv`

## 7. 注意事项

- API密钥请妥善保管，不要提交到代码仓库
- 注意API调用频率限制
- 不同模型有不同的token限制
- 图像理解功能需要使用glm-4v模型
