import asyncio

async def producer(queue):
    for i in range(5):
        await asyncio.sleep(1)
        await queue.put(i)
        print(f"Produced {i}")
    print("Producer finished")

async def consumer(name, queue):
    while True:
        try:
            # 使用超时避免无限等待
            item = await asyncio.wait_for(queue.get(), timeout=3.0)
            print(f"{name} consumed {item}")
            await asyncio.sleep(0.5)  # 模拟处理时间
            queue.task_done()
        except asyncio.TimeoutError:
            print(f"{name} timeout, stopping")
            break

async def main():
    queue = asyncio.Queue(maxsize=3)  # 限制队列大小
    
    # 启动生产者
    producer_task = asyncio.create_task(producer(queue))
    
    # 启动多个消费者
    consumer_tasks = [
        asyncio.create_task(consumer("Consumer-1", queue)),
        asyncio.create_task(consumer("Consumer-2", queue))
    ]
    
    # 等待生产者完成
    await producer_task
    
    # 等待队列中所有任务完成
    await queue.join()
    
    # 取消消费者任务
    for task in consumer_tasks:
        task.cancel()
    
    print("All tasks completed")

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"总耗时: {end - start:.2f} 秒")
