import asyncio
import logging

import sfdc

from models.tenant import TenantCreateEvent

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
            t = TenantCreateEvent(message['data']['payload'])
            logging.info(f"SFDC Tenant Create Event Received - Self Service Entry Id: {t.ssentry_id} - tenant_id: {t.tenant_id}")

            await event_queue.put(t)
