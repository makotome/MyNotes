from contextlib import contextmanager
import logging

# 配置logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 方法1：使用类实现上下文管理器
class MyContextManager:
    def __enter__(self):
        """进入with块时调用"""
        logger.info("开始执行")
        return self  # 返回值会赋给as后的变量
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开with块时调用"""
        logger.info("结束执行")
        return False  # 返回False表示不抑制异常

# 方法2：使用contextmanager装饰器实现函数形式的上下文管理器
@contextmanager
def my_context():
    """基于函数的上下文管理器"""
    try:
        logger.info("函数形式：开始执行")
        yield "这是yield的值"  # yield前的代码相当于__enter__
    finally:
        logger.info("函数形式：结束执行")  # yield后的代码相当于__exit__

def main():
    """
    主函数 - 程序的入口点
    """
    logger.info("程序开始运行")
    
    # 演示类形式的上下文管理器
    logger.info("=== 类形式的上下文管理器 ===")
    with MyContextManager() as cm:
        logger.info("在with块中")
        logger.debug(f"cm对象类型: {type(cm)}")
    
    # 演示函数形式的上下文管理器
    logger.info("=== 函数形式的上下文管理器 ===")
    with my_context() as value:
        logger.info(f"在with块中，接收到的值：{value}")
    
    logger.info("程序执行完毕")

if __name__ == "__main__":
    main()
    print("\n程序执行完毕")

if __name__ == "__main__":
    main()