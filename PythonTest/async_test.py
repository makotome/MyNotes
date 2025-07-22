import asyncio
import time

lock = asyncio.Lock()

async def shared_resource(name):
    async with lock:
        print(f"{name} 访问共享资源")
        await asyncio.sleep(2)  # 模拟异步操作
        print(f"{name} 完成访问共享资源")

async def main():
    await asyncio.gather(
        shared_resource("任务1"),
        shared_resource("任务2"),
        shared_resource("任务3")
    )

if __name__ == "__main__":
    import time
    # 开始时间
    start = time.perf_counter()
    asyncio.run(main())
    # 结束时间
    end = time.perf_counter()
    print(f"总耗时: {end - start:.2f} 秒")