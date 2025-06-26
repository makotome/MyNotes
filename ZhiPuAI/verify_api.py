"""
智谱AI API密钥验证工具
用于快速测试API密钥是否有效
"""

import os
from zhipuai import ZhipuAI
from dotenv import load_dotenv

def test_api_key():
    """测试API密钥是否有效"""
    # 加载环境变量
    load_dotenv()
    
    # 获取API密钥
    api_key = os.getenv('ZHIPUAI_API_KEY')
    
    if not api_key:
        print("❌ 错误：在.env文件中未找到ZHIPUAI_API_KEY")
        print("请确保.env文件存在并包含：")
        print("ZHIPUAI_API_KEY=your_actual_api_key")
        return False
    
    print(f"🔑 找到API密钥：{api_key[:10]}...{api_key[-10:]}")
    
    try:
        # 创建客户端
        client = ZhipuAI(api_key=api_key)
        
        # 发送简单测试请求
        print("🚀 正在测试API连接...")
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "user", "content": "你好"}
            ],
            max_tokens=10
        )
        
        print("✅ API密钥验证成功！")
        print(f"📄 AI回复：{response.choices[0].message.content}")
        print(f"📊 使用token：{response.usage}")
        return True
        
    except Exception as e:
        print(f"❌ API密钥验证失败：{str(e)}")
        
        # 提供详细的错误诊断
        if "401" in str(e):
            print("\n🔧 错误诊断：")
            print("1. 检查API密钥是否正确")
            print("2. 检查API密钥是否已过期")
            print("3. 登录智谱AI控制台确认密钥状态：https://bigmodel.cn/console/overview")
        elif "网络" in str(e) or "timeout" in str(e).lower():
            print("\n🔧 网络连接问题，请检查网络设置")
        else:
            print(f"\n🔧 其他错误：{str(e)}")
        
        return False

def get_model_list():
    """获取可用模型列表"""
    # 加载环境变量
    load_dotenv()
    
    # 获取API密钥
    api_key = os.getenv('ZHIPUAI_API_KEY')
    
    if not api_key:
        print("❌ 错误：在.env文件中未找到ZHIPUAI_API_KEY")
        return False
    
    try:
        # 创建客户端
        client = ZhipuAI(api_key=api_key)
        
        # 智谱AI的SDK可能不直接提供模型列表API，我们通过测试常用模型来验证可用性
        print("📋 正在测试常用模型可用性...")
        
        print("✅ 正在检测可用模型：")
        print("=" * 60)
        
        # 测试常用模型
        test_models = [
            "glm-4",
            "glm-4-flash", 
            "glm-4v",
            "glm-3-turbo",
            "chatglm_turbo",
            "chatglm_std",
            "chatglm_lite"
        ]
        
        available_models = []
        
        for model_id in test_models:
            try:
                print(f"🔍 测试模型: {model_id}...", end=" ")
                # 发送简单测试请求来验证模型是否可用
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": "hi"}],
                    max_tokens=1
                )
                print("✅ 可用")
                available_models.append(model_id)
            except Exception as e:
                if "model" in str(e).lower() or "not found" in str(e).lower():
                    print("❌ 不可用")
                else:
                    print(f"⚠️  未知错误: {str(e)[:50]}...")
        
        print(f"\n🎯 检测到 {len(available_models)} 个可用模型")
        print("-" * 40)
        
        # 显示常用模型信息
        print("\n📊 常用模型说明：")
        print("=" * 60)
        common_models = {
            "glm-4": "GLM-4 标准版 - 最新的对话模型",
            "glm-4-flash": "GLM-4 Flash - 轻量级快速响应版本（通常免费额度较多）",
            "glm-4v": "GLM-4V - 支持图像理解的多模态模型",
            "glm-3-turbo": "GLM-3 Turbo - 高性价比版本",
            "chatglm_turbo": "ChatGLM Turbo - 经济实惠版本",
            "chatglm_std": "ChatGLM 标准版",
            "chatglm_lite": "ChatGLM 轻量版 - 通常有免费额度"
        }
        
        for model_id, description in common_models.items():
            print(f"• {model_id}: {description}")
        
        print("\n💡 免费额度说明：")
        print("- 新用户通常会获得一定的免费tokens")
        print("- glm-4-flash 和 chatglm_lite 通常有较多免费额度")
        print("- 具体免费额度请查看智谱AI控制台：https://bigmodel.cn/console/overview")
        
        if available_models:
            print(f"\n🎉 您的账户可以使用以下模型：")
            for model in available_models:
                desc = common_models.get(model, "")
                print(f"✅ {model} - {desc}")
        else:
            print("\n⚠️  未检测到可用模型，请检查API密钥权限")
        
        return True
        
    except Exception as e:
        print(f"❌ 获取模型列表失败：{str(e)}")
        return False

def main():
    """主函数"""
    print("🎯 智谱AI API密钥验证工具")
    print("=" * 40)
    
    # 选择功能
    print("\n请选择功能：")
    print("1. 验证API密钥")
    print("2. 获取模型列表")
    print("3. 同时执行以上两项")
    
    choice = input("\n请输入选择 (1/2/3，默认为3): ").strip()
    if not choice:
        choice = "3"
    
    success = True
    
    if choice in ["1", "3"]:
        print("\n" + "=" * 40)
        if test_api_key():
            print("\n🎉 API密钥验证成功！")
        else:
            print("\n❌ API密钥验证失败！")
            success = False
    
    if choice in ["2", "3"] and (choice != "3" or success):
        print("\n" + "=" * 40)
        if get_model_list():
            print("\n🎉 模型列表获取成功！")
        else:
            print("\n❌ 模型列表获取失败！")
            success = False
    
    if success:
        print("\n✨ 所有操作完成！")
    else:
        print("\n❌ 部分操作失败，请检查配置后重试。")

if __name__ == "__main__":
    main()
