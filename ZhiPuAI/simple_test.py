"""
简单的智谱AI测试示例
适合快速上手测试
"""

import os
from zhipuai import ZhipuAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置API密钥（从环境变量中获取）
API_KEY = os.getenv('ZHIPUAI_API_KEY')

if not API_KEY:
    print("❌ 错误：请在.env文件中设置ZHIPUAI_API_KEY")
    exit(1)

def simple_chat_test():
    """简单的聊天测试"""
    # 初始化客户端
    client = ZhipuAI(api_key=API_KEY)
    
    # 发送消息
    response = client.chat.completions.create(
        model="glm-4",  # 可选：glm-4, glm-4v, glm-3-turbo
        messages=[
            {"role": "user", "content": "你好，请介绍一下智谱AI"}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    # 打印结果
    print("AI回复:", response.choices[0].message.content)
    print("使用token:", response.usage)

def stream_chat_test():
    """流式聊天测试"""
    client = ZhipuAI(api_key=API_KEY)
    
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "user", "content": "请写一首关于人工智能的诗"}
        ],
        stream=True  # 开启流式输出
    )
    
    print("AI回复（流式）:")
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()

if __name__ == "__main__":
    print("开始测试智谱AI...")
    
    # 基础聊天测试
    print("\n=== 基础聊天测试 ===")
    simple_chat_test()
    
    # 流式聊天测试
    print("\n=== 流式聊天测试 ===")
    stream_chat_test()
