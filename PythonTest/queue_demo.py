import asyncio

async def producer(queue):
    for i in range(3):
        await asyncio.sleep(1)
        await queue.put(i)
        print(f"Produced {i}")
    
    # 发送结束信号
    await queue.put(None)  # 哨兵值
    print("Producer finished")

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:  # 收到结束信号
            print("Consumer finished")
            queue.task_done()
            break
        
        print(f"Consumed {item}")
        await asyncio.sleep(0.5)  # 模拟处理时间
        queue.task_done()  # 标记任务完成

async def main():
    queue = asyncio.Queue()
    
    # 创建生产者和消费者任务
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    
    # 等待所有任务完成
    await asyncio.gather(producer_task, consumer_task)

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"总耗时: {end - start:.2f} 秒")
