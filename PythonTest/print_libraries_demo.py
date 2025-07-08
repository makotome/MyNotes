#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
常用Python打印库示例
"""

import logging
import sys
from datetime import datetime

# =============================================================================
# 1. logging - 最推荐的方式
# =============================================================================
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('demo.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def demo_logging():
    """演示logging的使用"""
    print("\n" + "="*50)
    print("1. LOGGING 库演示")
    print("="*50)
    
    logger.debug("这是调试信息")
    logger.info("这是普通信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    logger.critical("这是严重错误信息")
    
    # 可以记录异常
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        logger.exception("捕获到异常:")  # 自动记录堆栈信息

# =============================================================================
# 2. rich - 美化输出（需要安装：pip install rich）
# =============================================================================
def demo_rich():
    """演示rich库的使用"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.progress import track
        from rich.panel import Panel
        from rich.text import Text
        import time
        
        print("\n" + "="*50)
        print("2. RICH 库演示")
        print("="*50)
        
        console = Console()
        
        # 彩色文本
        console.print("Hello", style="bold red")
        console.print("World", style="bold blue")
        
        # 表格
        table = Table(title="示例表格")
        table.add_column("姓名", style="cyan")
        table.add_column("年龄", style="magenta")
        table.add_column("城市", style="green")
        
        table.add_row("张三", "25", "北京")
        table.add_row("李四", "30", "上海")
        console.print(table)
        
        # 面板
        console.print(Panel("这是一个面板", title="提示"))
        
        # 进度条
        for i in track(range(10), description="处理中..."):
            time.sleep(0.1)
            
    except ImportError:
        print("rich库未安装，跳过演示")
        print("安装命令: pip install rich")

# =============================================================================
# 3. colorama - 跨平台彩色输出（需要安装：pip install colorama）
# =============================================================================
def demo_colorama():
    """演示colorama库的使用"""
    try:
        from colorama import init, Fore, Back, Style
        init()  # 初始化colorama
        
        print("\n" + "="*50)
        print("3. COLORAMA 库演示")
        print("="*50)
        
        print(Fore.RED + "这是红色文字")
        print(Fore.GREEN + "这是绿色文字")
        print(Fore.BLUE + "这是蓝色文字")
        print(Back.YELLOW + "这是黄色背景")
        print(Style.BRIGHT + "这是亮色文字")
        print(Style.RESET_ALL + "重置所有样式")
        
    except ImportError:
        print("colorama库未安装，跳过演示")
        print("安装命令: pip install colorama")

# =============================================================================
# 4. tqdm - 进度条（需要安装：pip install tqdm）
# =============================================================================
def demo_tqdm():
    """演示tqdm进度条的使用"""
    try:
        from tqdm import tqdm
        import time
        
        print("\n" + "="*50)
        print("4. TQDM 进度条演示")
        print("="*50)
        
        # 基本进度条
        for i in tqdm(range(20), desc="基本进度条"):
            time.sleep(0.1)
            
        # 自定义进度条
        items = ["任务1", "任务2", "任务3", "任务4", "任务5"]
        for item in tqdm(items, desc="处理任务", unit="个"):
            time.sleep(0.3)
            tqdm.write(f"正在处理: {item}")
            
    except ImportError:
        print("tqdm库未安装，跳过演示")
        print("安装命令: pip install tqdm")

# =============================================================================
# 5. pprint - 美化打印Python对象
# =============================================================================
def demo_pprint():
    """演示pprint的使用"""
    from pprint import pprint
    
    print("\n" + "="*50)
    print("5. PPRINT 美化打印演示")
    print("="*50)
    
    # 复杂数据结构
    data = {
        'users': [
            {'name': '张三', 'age': 25, 'hobbies': ['读书', '游戏', '音乐']},
            {'name': '李四', 'age': 30, 'hobbies': ['运动', '旅行']},
        ],
        'settings': {
            'theme': 'dark',
            'language': 'zh-cn',
            'features': {
                'notifications': True,
                'auto_save': False
            }
        }
    }
    
    print("普通print:")
    print(data)
    
    print("\npprint美化输出:")
    pprint(data, width=60, depth=3)

# =============================================================================
# 6. 自定义打印函数
# =============================================================================
def custom_print(message, level="INFO", timestamp=True):
    """自定义打印函数"""
    colors = {
        "INFO": "\033[92m",      # 绿色
        "WARNING": "\033[93m",   # 黄色
        "ERROR": "\033[91m",     # 红色
        "DEBUG": "\033[94m",     # 蓝色
    }
    reset = "\033[0m"
    
    prefix = ""
    if timestamp:
        prefix += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
    
    color = colors.get(level, "")
    print(f"{color}{prefix}[{level}] {message}{reset}")

def demo_custom_print():
    """演示自定义打印函数"""
    print("\n" + "="*50)
    print("6. 自定义打印函数演示")
    print("="*50)
    
    custom_print("这是普通信息")
    custom_print("这是警告信息", "WARNING")
    custom_print("这是错误信息", "ERROR")
    custom_print("这是调试信息", "DEBUG")
    custom_print("无时间戳信息", "INFO", timestamp=False)

# =============================================================================
# 主函数
# =============================================================================
def main():
    """主函数"""
    print("Python 常用打印库演示")
    print("=" * 80)
    
    # 演示各种打印库
    demo_logging()
    demo_rich()
    demo_colorama()
    demo_tqdm()
    demo_pprint()
    demo_custom_print()
    
    print("\n" + "="*80)
    print("演示完成！")
    print("推荐使用顺序:")
    print("1. logging - 用于正式项目的日志记录")
    print("2. rich - 用于CLI工具的美化输出")
    print("3. tqdm - 用于显示处理进度")
    print("4. pprint - 用于调试时美化打印复杂对象")
    print("5. colorama - 用于简单的彩色输出")

if __name__ == "__main__":
    main()
