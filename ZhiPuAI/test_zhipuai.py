"""
智谱AI模型测试脚本
测试智谱AI的各种模型功能
"""

import os
import json
from zhipuai import ZhipuAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ZhipuAITester:
    def __init__(self):
        """初始化智谱AI客户端"""
        self.api_key = os.getenv('ZHIPUAI_API_KEY')
        if not self.api_key:
            raise ValueError("请在.env文件中设置ZHIPUAI_API_KEY")
        
        self.client = ZhipuAI(api_key=self.api_key)
        
    def test_chat_completion(self, model="glm-4", messages=None):
        """
        测试聊天补全功能
        
        Args:
            model (str): 模型名称，如 "glm-4", "glm-4v", "glm-3-turbo" 等
            messages (list): 消息列表
        """
        if messages is None:
            messages = [
                {"role": "user", "content": "你好，请介绍一下你自己"}
            ]
        
        print(f"🚀 测试模型: {model}")
        print(f"📝 输入消息: {json.dumps(messages, ensure_ascii=False, indent=2)}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                stream=False
            )
            
            print("✅ 请求成功！")
            print(f"📄 响应内容: {response.choices[0].message.content}")
            print(f"📊 使用token: {response.usage}")
            print("-" * 50)
            
            return response
            
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            return None
    
    def test_stream_chat(self, model="glm-4", messages=None):
        """
        测试流式聊天功能
        
        Args:
            model (str): 模型名称
            messages (list): 消息列表
        """
        if messages is None:
            messages = [
                {"role": "user", "content": "请写一首关于春天的诗"}
            ]
        
        print(f"🌊 测试流式模型: {model}")
        print(f"📝 输入消息: {json.dumps(messages, ensure_ascii=False, indent=2)}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                stream=True
            )
            
            print("✅ 流式请求开始！")
            print("📄 响应内容: ", end="")
            
            full_content = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_content += content
            
            print("\n✅ 流式响应完成！")
            print("-" * 50)
            
            return full_content
            
        except Exception as e:
            print(f"❌ 流式请求失败: {str(e)}")
            return None
    
    def test_function_calling(self, model="glm-4"):
        """
        测试函数调用功能
        """
        # 定义函数
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "获取指定城市的天气信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名称"
                            }
                        },
                        "required": ["city"]
                    }
                }
            }
        ]
        
        messages = [
            {"role": "user", "content": "北京今天天气怎么样？"}
        ]
        
        print(f"🔧 测试函数调用功能: {model}")
        print(f"📝 输入消息: {json.dumps(messages, ensure_ascii=False, indent=2)}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            print("✅ 函数调用请求成功！")
            
            # 检查是否有工具调用
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    print(f"🔧 调用函数: {tool_call.function.name}")
                    print(f"📋 函数参数: {tool_call.function.arguments}")
            else:
                print(f"📄 普通响应: {response.choices[0].message.content}")
            
            print("-" * 50)
            return response
            
        except Exception as e:
            print(f"❌ 函数调用失败: {str(e)}")
            return None
    
    def test_vision_model(self, model="glm-4v"):
        """
        测试视觉模型功能（需要图片URL）
        """
        # 使用一个示例图片URL
        image_url = "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto"
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "请描述这张图片的内容"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
        
        print(f"👁️ 测试视觉模型: {model}")
        print(f"🖼️ 图片URL: {image_url}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            print("✅ 视觉模型请求成功！")
            print(f"📄 图片描述: {response.choices[0].message.content}")
            print("-" * 50)
            
            return response
            
        except Exception as e:
            print(f"❌ 视觉模型请求失败: {str(e)}")
            return None
    
    def run_comprehensive_test(self):
        """运行全面测试"""
        print("🎯 开始智谱AI全面测试...")
        print("=" * 60)
        
        # 1. 基础聊天测试
        print("1️⃣ 基础聊天测试")
        self.test_chat_completion("glm-4")
        
        # 2. 流式聊天测试
        print("2️⃣ 流式聊天测试")
        self.test_stream_chat("glm-4")
        
        # 3. 不同模型测试
        print("3️⃣ 测试不同模型")
        models_to_test = ["glm-4", "glm-3-turbo"]
        for model in models_to_test:
            messages = [{"role": "user", "content": f"请用一句话介绍{model}模型"}]
            self.test_chat_completion(model, messages)
        
        # 4. 函数调用测试
        print("4️⃣ 函数调用测试")
        self.test_function_calling("glm-4")
        
        # 5. 视觉模型测试（如果支持）
        print("5️⃣ 视觉模型测试")
        self.test_vision_model("glm-4v")
        
        print("🎉 全面测试完成！")

def main():
    """主函数"""
    try:
        # 创建测试实例
        tester = ZhipuAITester()
        
        # 运行全面测试
        tester.run_comprehensive_test()
        
        # 或者单独测试某个功能
        # tester.test_chat_completion("glm-4", [{"role": "user", "content": "Hello!"}])
        # tester.test_stream_chat("glm-4")
        # tester.test_function_calling("glm-4")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")

if __name__ == "__main__":
    main()
