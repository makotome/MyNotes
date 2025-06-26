"""
智谱AI函数调用完整示例
演示如何实现真正的函数调用功能
"""

import os
import json
import requests
from zhipuai import ZhipuAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class WeatherFunctionDemo:
    def __init__(self):
        """初始化"""
        self.api_key = os.getenv('ZHIPUAI_API_KEY')
        if not self.api_key:
            raise ValueError("请在.env文件中设置ZHIPUAI_API_KEY")
        
        self.client = ZhipuAI(api_key=self.api_key)
    
    def get_weather(self, city):
        """
        真正的天气获取函数
        这是一个模拟函数，实际项目中可以调用真实的天气API
        """
        # 模拟天气数据
        weather_data = {
            "北京": {"temperature": "22°C", "weather": "晴天", "humidity": "45%"},
            "上海": {"temperature": "26°C", "weather": "多云", "humidity": "60%"},
            "广州": {"temperature": "28°C", "weather": "小雨", "humidity": "75%"},
            "深圳": {"temperature": "27°C", "weather": "阴天", "humidity": "70%"},
        }
        
        # 如果城市不在数据中，返回默认信息
        if city not in weather_data:
            return f"抱歉，暂时无法获取{city}的天气信息"
        
        data = weather_data[city]
        return f"{city}今天的天气：{data['weather']}，温度{data['temperature']}，湿度{data['humidity']}"
    
    def get_current_time(self, timezone="Asia/Shanghai"):
        """
        获取当前时间的函数
        """
        from datetime import datetime
        
        # 简化版本，不使用pytz
        current_time = datetime.now()
        return current_time.strftime("%Y年%m月%d日 %H:%M:%S")
    
    def demo_function_calling(self):
        """
        演示完整的函数调用流程
        """
        # 定义可用的函数工具
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
                                "description": "城市名称，如：北京、上海等"
                            }
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "get_current_time",
                    "description": "获取当前时间",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "description": "时区，默认为Asia/Shanghai"
                            }
                        },
                        "required": []
                    }
                }
            }
        ]
        
        # 用户问题
        user_question = "北京今天天气怎么样？现在几点了？"
        
        messages = [
            {"role": "user", "content": user_question}
        ]
        
        print(f"👤 用户问题: {user_question}")
        print("🤖 AI 分析中...")
        
        # 第一次调用：让AI决定是否需要调用函数
        response = self.client.chat.completions.create(
            model="glm-4",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        # 检查AI是否想要调用函数
        if response.choices[0].message.tool_calls:
            print("🔧 AI 决定调用函数:")
            
            # 先将AI的响应添加到对话历史
            assistant_message = {
                "role": "assistant",
                "content": response.choices[0].message.content,
                "tool_calls": []
            }
            
            # 处理每个函数调用
            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"   函数名: {function_name}")
                print(f"   参数: {function_args}")
                
                # 执行对应的真实函数
                if function_name == "get_weather":
                    result = self.get_weather(function_args.get("city", ""))
                elif function_name == "get_current_time":
                    result = self.get_current_time(function_args.get("timezone", "Asia/Shanghai"))
                else:
                    result = f"未知函数: {function_name}"
                
                print(f"   执行结果: {result}")
                
                # 添加工具调用信息到assistant消息
                assistant_message["tool_calls"].append({
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                })
                
                # 添加工具执行结果
                messages.append(assistant_message)
                messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_call_id": tool_call.id
                })
            
            # 第二次调用：让AI基于函数结果生成最终回答
            print("\n🤖 生成最终回答...")
            try:
                final_response = self.client.chat.completions.create(
                    model="glm-4",
                    messages=messages,
                    temperature=0.7
                )
                
                print(f"✅ 最终回答: {final_response.choices[0].message.content}")
            except Exception as e:
                print(f"❌ 生成最终回答时出错: {str(e)}")
                print(f"📝 调试信息 - 消息历史长度: {len(messages)}")
        
        else:
            # AI没有调用函数，直接回答
            print(f"💬 直接回答: {response.choices[0].message.content}")

def main():
    """主函数"""
    print("🌟 智谱AI函数调用完整演示")
    print("=" * 50)
    
    try:
        demo = WeatherFunctionDemo()
        demo.demo_function_calling()
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

if __name__ == "__main__":
    main()
