"""
智谱AI函数调用简化版演示
解决序列化问题的完整示例
"""

import os
import json
from zhipuai import ZhipuAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SimpleFunctionDemo:
    def __init__(self):
        """初始化"""
        self.api_key = os.getenv('ZHIPUAI_API_KEY')
        if not self.api_key:
            raise ValueError("请在.env文件中设置ZHIPUAI_API_KEY")
        
        self.client = ZhipuAI(api_key=self.api_key)
    
    def get_weather(self, city):
        """真正的天气获取函数"""
        weather_data = {
            "北京": {"temperature": "22°C", "weather": "晴天", "humidity": "45%"},
            "上海": {"temperature": "26°C", "weather": "多云", "humidity": "60%"},
            "广州": {"temperature": "28°C", "weather": "小雨", "humidity": "75%"},
            "深圳": {"temperature": "27°C", "weather": "阴天", "humidity": "70%"},
        }
        
        if city not in weather_data:
            return f"抱歉，暂时无法获取{city}的天气信息"
        
        data = weather_data[city]
        return f"{city}今天的天气：{data['weather']}，温度{data['temperature']}，湿度{data['humidity']}"
    
    def get_current_time(self):
        """获取当前时间"""
        from datetime import datetime
        current_time = datetime.now()
        return current_time.strftime("%Y年%m月%d日 %H:%M:%S")
    
    def simple_function_calling(self):
        """简化的函数调用演示"""
        
        # 定义工具
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
        
        # 用户问题
        user_question = "北京今天天气怎么样？"
        
        print(f"👤 用户问题: {user_question}")
        print("🤖 AI 分析中...")
        
        # 调用AI
        response = self.client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": user_question}],
            tools=tools,
            tool_choice="auto"
        )
        
        # 检查是否有函数调用
        if response.choices[0].message.tool_calls:
            print("🔧 AI 决定调用函数:")
            
            all_results = []
            
            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"   函数名: {function_name}")
                print(f"   参数: {function_args}")
                
                # 执行函数
                if function_name == "get_weather":
                    result = self.get_weather(function_args.get("city", ""))
                    all_results.append(f"天气信息：{result}")
                    print(f"   执行结果: {result}")
            
            # 简化方式：直接用函数结果让AI生成回答
            if all_results:
                print("\n🤖 生成最终回答...")
                
                final_prompt = f"""
用户问题：{user_question}

函数执行结果：
{chr(10).join(all_results)}

请根据上述信息，用自然语言回答用户的问题。
"""
                
                final_response = self.client.chat.completions.create(
                    model="glm-4",
                    messages=[{"role": "user", "content": final_prompt}],
                    temperature=0.7
                )
                
                print(f"✅ 最终回答: {final_response.choices[0].message.content}")
        
        else:
            # 没有函数调用
            print(f"💬 直接回答: {response.choices[0].message.content}")
    
    def step_by_step_demo(self):
        """分步演示函数调用过程"""
        print("📚 分步演示函数调用过程")
        print("=" * 40)
        
        # 步骤1：定义函数
        print("1️⃣ 定义可用函数")
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather", 
                    "description": "获取城市天气",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "城市名"}
                        },
                        "required": ["city"]
                    }
                }
            }
        ]
        print("   ✅ 已定义 get_weather 函数")
        
        # 步骤2：用户提问
        print("\n2️⃣ 用户提问")
        question = "上海的天气如何？"
        print(f"   用户: {question}")
        
        # 步骤3：AI分析
        print("\n3️⃣ AI分析并决定")
        response = self.client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": question}],
            tools=tools,
            tool_choice="auto"
        )
        
        if response.choices[0].message.tool_calls:
            print("   ✅ AI决定调用函数")
            
            # 步骤4：解析函数调用
            print("\n4️⃣ 解析函数调用")
            tool_call = response.choices[0].message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"   函数名: {function_name}")
            print(f"   参数: {function_args}")
            
            # 步骤5：执行真实函数
            print("\n5️⃣ 执行真实函数")
            city = function_args.get("city", "")
            result = self.get_weather(city)
            print(f"   执行结果: {result}")
            
            # 步骤6：生成最终回答
            print("\n6️⃣ 生成最终回答")
            final_prompt = f"用户问：{question}\n天气信息：{result}\n请用自然语言回答。"
            
            final_response = self.client.chat.completions.create(
                model="glm-4",
                messages=[{"role": "user", "content": final_prompt}]
            )
            
            print(f"   最终回答: {final_response.choices[0].message.content}")
        
        else:
            print("   ❌ AI没有调用函数")
            print(f"   直接回答: {response.choices[0].message.content}")

def main():
    """主函数"""
    print("🌟 智谱AI函数调用简化演示")
    print("=" * 50)
    
    try:
        demo = SimpleFunctionDemo()
        
        # 简单演示
        demo.simple_function_calling()
        
        print("\n" + "=" * 50)
        
        # 分步演示
        demo.step_by_step_demo()
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

if __name__ == "__main__":
    main()
