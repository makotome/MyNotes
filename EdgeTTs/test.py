import os
import sys
import edge_tts
import asyncio


example_text = "哈啰啊，我是小智啦，声音好听的台湾女孩一枚，超开心认识你耶，最近在忙啥，别忘了给我来点有趣的料哦，我超爱听八卦的啦"

async def list_voices():
    """列出所有可用的声音"""
    print("正在获取 EdgeTTS 支持的声音列表...")
    voices = await edge_tts.list_voices()
    
    print(f"\n找到 {len(voices)} 个可用声音：\n")
    
    # 按语言分组显示
    language_groups = {}
    for voice in voices:
        lang = voice['Locale']
        if lang not in language_groups:
            language_groups[lang] = []
        language_groups[lang].append(voice)
    
    for lang, lang_voices in sorted(language_groups.items()):
        print(f"=== {lang} ===")
        for voice in lang_voices:
            gender = voice.get('Gender', 'Unknown')
            name = voice.get('Name', 'Unknown')
            short_name = voice.get('ShortName', 'Unknown')
            print(f"  {short_name} ({gender}) - {name}")
        print()

async def list_chinese_voices():
    """只列出中文声音"""
    print("正在获取中文声音列表...")
    voices = await edge_tts.list_voices()
    
    # 筛选中文声音
    chinese_voices = [v for v in voices if 'zh-' in v['Locale']]
    
    print(f"\n找到 {len(chinese_voices)} 个中文声音：\n")
    
    for voice in chinese_voices:
        gender = voice.get('Gender', 'Unknown')
        name = voice.get('Name', 'Unknown')
        short_name = voice.get('ShortName', 'Unknown')
        locale = voice.get('Locale', 'Unknown')
        print(f"  {short_name} ({gender}, {locale}) - {name}")

async def use_chinese_voice():
    """使用中文声音朗读示例文本"""
    chinese_voices = await edge_tts.list_voices()
    chinese_voices = [v for v in chinese_voices if 'zh-' in v['Locale']]
    
    if not chinese_voices:
        print("没有找到中文声音")
        return
    
    # 选择第一个中文声音
    voice = chinese_voices[0]
    voice_name = voice.get('ShortName', 'Unknown')
    
    print(f"使用声音: {voice_name}")
    await speak_text(example_text, voice_name)

async def speak_text(text, voice_name):
    """使用指定声音朗读文本并保存为音频文件"""
    print(f"正在使用 {voice_name} 生成语音...")
    
    # 创建 Communicate 对象
    communicate = edge_tts.Communicate(text, voice_name)
    
    # 保存音频文件
    output_file = "output.mp3"
    await communicate.save(output_file)
    print(f"音频已保存为: {output_file}")

async def play_chinese_voice_text():
    """使用中文声音朗读示例文本并直接播放"""
    chinese_voices = await edge_tts.list_voices()
    chinese_voices = [v for v in chinese_voices if 'zh-' in v['Locale']]

    if not chinese_voices:
        print("没有找到中文声音")
        return
    
    # 打印所有中文声音
    print(f"\n找到 {len(chinese_voices)} 个中文声音：\n")
    for i, voice in enumerate(chinese_voices, start=1):
        gender = voice.get('Gender', 'Unknown')
        name = voice.get('Name', 'Unknown')
        short_name = voice.get('ShortName', 'Unknown')
        locale = voice.get('Locale', 'Unknown')
        print(f"  {i}. {short_name} ({gender}, {locale}) - {name}")

    choice = input(f"请输入选择 (1 - {len(chinese_voices)}): ").strip()

    # 选择对应的中文声音
    voice = chinese_voices[int(choice) - 1]
    voice_name = voice.get('ShortName', 'Unknown')

    print(f"使用声音: {voice_name}")
    await play_text(example_text, voice_name)

async def play_text(text, voice_name):
    """使用指定声音朗读文本并直接播放"""
    print(f"正在使用 {voice_name} 生成并播放语音...")
    
    # 创建 Communicate 对象
    communicate = edge_tts.Communicate(text, voice_name)
    
    # 流式获取音频数据
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    
    # 保存临时文件并播放
    temp_file = "temp_audio.mp3"
    with open(temp_file, "wb") as f:
        f.write(audio_data)
    
    print(f"临时音频文件已生成: {temp_file}")
    print("可以使用系统默认播放器播放此文件")
    
    # 尝试使用系统命令播放（macOS）
    import subprocess
    try:
        subprocess.run(["afplay", temp_file], check=True)
        print("音频播放完成")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("无法自动播放，请手动打开音频文件")
    
    # 清理临时文件
    import os
    if os.path.exists(temp_file):
        os.remove(temp_file)

async def amain():
    print("EdgeTTs Test Script")
    print("选择操作：")
    print("1. 列出所有声音")
    print("2. 只列出中文声音")
    print("3. 使用中文声音朗读示例文本(保存文件)")
    print("4. 使用中文声音朗读示例文本(直接播放)")
    
    try:
        choice = input("请输入选择 (1 - 4): ").strip()

        if choice == "1":
            await list_voices()
        elif choice == "2":
            await list_chinese_voices()
        elif choice == "3":
            await use_chinese_voice()
        elif choice == "4":
            await play_chinese_voice_text()
        else:
            print("无效选择，默认显示中文声音")
            await list_chinese_voices()
            
    except KeyboardInterrupt:
        print("\n程序已取消")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    asyncio.run(amain())
