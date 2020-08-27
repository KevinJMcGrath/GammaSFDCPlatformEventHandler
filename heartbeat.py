import asyncio
import logging

import config


async def heart_beat():
    while True:
        logging.info('heartbeat...')
        await asyncio.sleep(config.HeartbeatDelay)