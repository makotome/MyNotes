# 一步程序测试

import asyncio
import time

async def main():
    print("开始")
    await asyncio.sleep(1)
    print("结束")
    print("总耗时: 1秒")

async def async_task(name, delay):
    print(f"任务 {name} 开始，预计耗时 {delay} 秒")
    await asyncio.sleep(delay)
    print(f"任务 {name} 完成")


async def main_with_tasks():
    print("开始执行多个异步任务")
    
    # 创建多个异步任务
    tasks = [
        async_task("A", 2),
        async_task("B", 3),
        async_task("C", 1)
    ]
    
    # 并发执行所有任务
    await asyncio.gather(*tasks)
    
    print("所有任务完成")

async def create_3_task():
    """创建并执行3个异步任务"""
    task1 = asyncio.create_task(async_task("Task 1", 2))
    task2 = asyncio.create_task(async_task("Task 2", 3))
    task3 = asyncio.create_task(async_task("Task 3", 1))
    
    # 等待所有任务完成
    await asyncio.gather(task1, task2, task3)
    return task1, task2, task3

# 异步函数示例
if __name__ == "__main__":
    start_time = time.time()
    # asyncio.run(main())
    # asyncio.run(main_with_tasks())
    
    # 正确的方式：在asyncio.run()中运行异步函数
    asyncio.run(create_3_task())
    
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f}秒")