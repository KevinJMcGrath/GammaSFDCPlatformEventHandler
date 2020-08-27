import asyncio

async def consume(async_queue: asyncio.Queue):
    while True:
        tenant_event = await async_queue.get()

