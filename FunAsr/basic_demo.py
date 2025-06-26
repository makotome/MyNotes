"""
SenseVoiceSmall 基础使用示例
支持本地模型路径
"""

try:
    from funasr import AutoModel  # type: ignore
    from funasr.utils.postprocess_utils import rich_transcription_postprocess  # type: ignore
except ImportError as e:
    print("❌ 未检测到 funasr 库，请先安装：pip install funasr")
    raise e

import os

class SenseVoiceDemo:
    def __init__(self, model_path=None, device="auto"):
        # 获取脚本所在目录，保证 base_dir 可用
        base_dir = os.path.dirname(os.path.abspath(__file__))
        """
        初始化 SenseVoiceSmall 模型
        
        Args:
            model_path (str): 本地模型路径或 ModelScope 模型ID
            device (str): 运行设备 "cuda:0", "cpu", "auto"
        """
        # 默认模型路径，请根据您的实际路径修改
        if model_path is None:
            # 获取脚本所在目录，方便搜索父目录下的 models 文件夹
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # 尝试本地模型路径或在线模型ID
            possible_paths = [
                os.path.join(base_dir, "models/SenseVoiceSmall"),      # 当前目录下 models
                "iic/SenseVoiceSmall",                                 # 在线模型ID
            ]
            
            # 检查本地模型路径（排除在线模型ID）
            for path in possible_paths[:-1]:
                expanded_path = os.path.expanduser(path)
                if os.path.exists(expanded_path):
                    model_path = expanded_path
                    break
            
            if model_path is None:
                # 本地未检测到模型，使用在线模型ID
                model_path = possible_paths[-1]
                print(f"⚠️  未在 {possible_paths[:-1]} 中找到本地模型，使用在线模型 {model_path}")
        
        self.model_path = model_path
        print(f"🔄 正在加载模型: {model_path}")
        # 检测本地 VAD 模型路径
        vad_model_name = "fsmn-vad"
        local_vad_path = os.path.join(base_dir, "models/speech_fsmn_vad_zh-cn-16k-common-pytorch")
        if os.path.exists(local_vad_path):
            vad_model_name = local_vad_path
            print(f"✅ 检测到本地 VAD 模型: {vad_model_name}")
        else:
            print(f"⚠️ 未检测到本地 VAD 模型，使用默认 VAD 模型: {vad_model_name}")
        
        # 检测是否为在线模型ID
        is_online = isinstance(model_path, str) and not os.path.isabs(model_path) and not os.path.exists(model_path)
        print(f"🔍 模型类型: {'在线模型' if is_online else '本地模型'}")
        init_kwargs = {
            "model": model_path,
            "trust_remote_code": is_online,
            "vad_model": vad_model_name,
            "vad_kwargs": {"max_single_segment_time": 30000},
            "device": device,
        }
        if is_online:
            # 在线模型，使用远程代码
            init_kwargs["remote_code"] = model_path
        # 初始化模型
        try:
            self.model = AutoModel(**init_kwargs)
            print("✅ 模型加载成功！")
            
        except Exception as e:
            print(f"❌ 模型加载失败: {str(e)}")
            print("💡 请检查：")
            print("   1. 模型路径是否正确")
            print("   2. 是否安装了所需依赖 (pip install -r requirements.txt)")
            print("   3. 网络连接是否正常（使用在线模型时）")
            raise e
    
    def transcribe_file(self, audio_path, language="auto", use_itn=True):
        """
        转录音频文件
        
        Args:
            audio_path (str): 音频文件路径
            language (str): 语言代码 "auto", "zh", "en", "yue", "ja", "ko"
            use_itn (bool): 是否使用逆文本标准化（数字、日期等转换）
        
        Returns:
            dict: 识别结果，包含文本、情感、事件等信息
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        print(f"🎵 正在识别音频: {audio_path}")
        print(f"🌐 语言设置: {language}")
        
        try:
            # 执行识别
            result = self.model.generate(
                input=audio_path,
                cache={},
                language=language,
                use_itn=use_itn,
                batch_size_s=60,  # 批处理大小
                merge_vad=True,   # 合并VAD结果
                merge_length_s=15,  # 合并长度
            )
            
            # 后处理文本
            if result and len(result) > 0:
                raw_text = result[0]["text"]
                processed_text = rich_transcription_postprocess(raw_text)
                
                # 解析结果
                result_dict = self._parse_result(raw_text, processed_text)
                return result_dict
            else:
                return {"error": "未识别到内容"}
                
        except Exception as e:
            print(f"❌ 识别失败: {str(e)}")
            return {"error": str(e)}
    
    def _parse_result(self, raw_text, processed_text):
        """
        解析识别结果，提取各种信息
        """
        result = {
            "text": processed_text,
            "raw_text": raw_text,
            "language": "unknown",
            "emotion": "unknown", 
            "events": [],
            "itn_applied": False
        }
        
        # 解析语言标签
        if "<|zh|>" in raw_text:
            result["language"] = "中文"
        elif "<|en|>" in raw_text:
            result["language"] = "英语"
        elif "<|yue|>" in raw_text:
            result["language"] = "粤语"
        elif "<|ja|>" in raw_text:
            result["language"] = "日语"
        elif "<|ko|>" in raw_text:
            result["language"] = "韩语"
        
        # 解析情感标签
        emotions = {
            "<|HAPPY|>": "开心",
            "<|SAD|>": "悲伤", 
            "<|ANGRY|>": "愤怒",
            "<|NEUTRAL|>": "中性",
            "<|FEARFUL|>": "恐惧",
            "<|DISGUSTED|>": "厌恶",
            "<|SURPRISED|>": "惊讶"
        }
        
        for tag, emotion in emotions.items():
            if tag in raw_text:
                result["emotion"] = emotion
                break
        
        # 解析音频事件
        events = {
            "<|BGM|>": "背景音乐",
            "<|Speech|>": "语音",
            "<|Applause|>": "掌声", 
            "<|Laughter|>": "笑声",
            "<|Cry|>": "哭声",
            "<|Sneeze|>": "打喷嚏",
            "<|Cough|>": "咳嗽"
        }
        
        for tag, event in events.items():
            if tag in raw_text:
                result["events"].append(event)
        
        # 检查是否应用了ITN
        if "<|withitn|>" in raw_text:
            result["itn_applied"] = True
        
        return result
    
    def batch_transcribe(self, audio_files, language="auto", use_itn=True):
        """
        批量转录多个音频文件
        """
        results = []
        total = len(audio_files)
        
        print(f"📁 开始批量处理 {total} 个音频文件...")
        
        for i, audio_path in enumerate(audio_files, 1):
            print(f"\n[{i}/{total}] 处理: {os.path.basename(audio_path)}")
            result = self.transcribe_file(audio_path, language, use_itn)
            result["file_path"] = audio_path
            results.append(result)
        
        print(f"\n✅ 批量处理完成！共处理 {total} 个文件")
        return results

def main():
    """演示基本用法"""
    print("🎯 SenseVoiceSmall 基础演示")
    print("=" * 50)
    
    # 请修改为您的实际模型路径
    MODEL_PATH = None  # 设置为 None 会自动搜索本地模型
    
    try:
        # 初始化模型
        demo = SenseVoiceDemo(model_path=MODEL_PATH, device="auto")
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 示例音频路径（请替换为您的实际音频文件）
        audio_files = [
            os.path.join(base_dir, "models/SenseVoiceSmall/example/zh.mp3"),
            os.path.join(base_dir, "models/SenseVoiceSmall/example/en.mp3"),
        ]

        print(f"📂 示例音频文件: {', '.join(audio_files)}")
        
        # 检查音频文件是否存在
        existing_files = [f for f in audio_files if os.path.exists(f)]
        
        if existing_files:
            # 单个文件转录
            print("\n1️⃣ 单个文件转录演示")
            result = demo.transcribe_file(existing_files[0], language="auto")
            print(f"📄 识别结果: {result}")
            
            # 批量转录
            if len(existing_files) > 1:
                print("\n2️⃣ 批量转录演示")
                batch_results = demo.batch_transcribe(existing_files[:2])
                for result in batch_results:
                    print(f"📁 {os.path.basename(result['file_path'])}: {result['text']}")
        else:
            print("⚠️  未找到示例音频文件")
            print("💡 请将音频文件路径修改为您的实际文件路径")
            print("支持格式: wav, mp3, flac, m4a 等")
            
            # 显示使用示例
            print("\n📖 使用示例:")
            print("demo = SenseVoiceDemo()")
            print('result = demo.transcribe_file("your_audio.wav")')
            print("print(result['text'])")
        
    except Exception as e:
        print(f"❌ 演示失败: {str(e)}")

if __name__ == "__main__":
    main()
