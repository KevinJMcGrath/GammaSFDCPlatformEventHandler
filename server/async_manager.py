import asyncio
import logging

from server import heartbeat
from server import platform_event_listener as pel
from server import platform_event_queue_processor as peq
# from server import tenant_build_monitor as tbm
from server import sym_completion_monitor as scm


platform_event_queue = asyncio.Queue()

async def gather_coroutines():
    await asyncio.gather(
        heartbeat.emit_heartbeat_signal(),
        pel.listen(platform_event_queue),
        peq.process_events(platform_event_queue),
        # tbm.monitor_tenants(),

        # TODO: Enable this when Spinnaker is properly setup to automate Edwin
        # scm.monitor_tenant_symphony_stream()
    )

def start_server():
    logging.info('Starting event loop...')
    loop = asyncio.get_event_loop()
    logging.info('Initiating async processes...')
    loop.run_until_complete(gather_coroutines())