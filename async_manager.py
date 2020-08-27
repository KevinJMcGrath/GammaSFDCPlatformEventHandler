import asyncio

import heartbeat
import sfdc

tenant_queue = asyncio.Queue()

async def gather_coroutines():
    await asyncio.gather(
        sfdc.PlatformEventsClient.stream_events(),
        heartbeat.heart_beat()
    )

def start_server():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_coroutines())