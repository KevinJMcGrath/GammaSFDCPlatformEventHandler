import asyncio
import logging

import config


async def emit_heartbeat_signal():
    while True:
        logging.info('heartbeat...')
        await asyncio.sleep(config.HeartbeatDelay)