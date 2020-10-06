import asyncio
import logging

import sfdc

from models.tenant import TenantEvent

# asyncio examples
    # Intro Guide: https://faculty.ai/blog/a-guide-to-using-asyncio/
    # Queues: https://stackoverflow.com/questions/34039588/asyncio-and-infinite-loop
    # Client-Server: https://stackoverflow.com/questions/31901425/python-asyncio-heartbeat-method-not-writing-to-stream
    # Gather: https://stackoverflow.com/questions/32054066/python-how-to-run-multiple-coroutines-concurrently-using-asyncio
async def listen(event_queue: asyncio.Queue):
    logging.info('Starting SFDC Platform Event Monitor.')
    # Setup Streaming Client as a context manager
    async with sfdc.PEListenerClient.client as c:

        # Add a subscription to the client
        await c.subscribe(sfdc.PEListenerClient.channel)

        async for message in c:
            t = TenantEvent(message['data']['payload'])
            logging.info(f"SFDC Tenant Event Received - type: {t.type}")

            await event_queue.put(t)
