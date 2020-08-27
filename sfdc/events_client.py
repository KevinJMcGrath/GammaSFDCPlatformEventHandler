import asyncio

import logging

from models.tenant import TenantCreateEvent

# https://aiosfstream.readthedocs.io/en/latest/quickstart.html
from aiosfstream import SalesforceStreamingClient

class EventsClient:
    def __init__(self, platform_config, tenant_queue: asyncio.Queue):
        self.client_key = platform_config['client_key']
        self.client_secret = platform_config['client_secret']
        self.username = platform_config['username']
        self.password = platform_config['password']
        self.security_token = platform_config['security_token']
        self.sandbox = platform_config['sandbox']
        self.channel = platform_config['event_channel']
        self.queue = tenant_queue

        self.client: SalesforceStreamingClient = self.init_client()

    # Create Platform Event
    # Endpoint: /services/data/v48.0/sobjects/Tenant_Event__e
    # https://developer.salesforce.com/docs/atlas.en-us.226.0.platform_events.meta/platform_events/platform_events_publish_api.htm
    def init_client(self):
        return SalesforceStreamingClient(consumer_key=self.client_key, consumer_secret=self.client_secret,
                                    username=self.username, password=self.password + self.security_token,
                                    sandbox=self.sandbox)

    # asyncio examples
    # Intro Guide: https://faculty.ai/blog/a-guide-to-using-asyncio/
    # Queues: https://stackoverflow.com/questions/34039588/asyncio-and-infinite-loop
    # Client-Server: https://stackoverflow.com/questions/31901425/python-asyncio-heartbeat-method-not-writing-to-stream
    # Gather: https://stackoverflow.com/questions/32054066/python-how-to-run-multiple-coroutines-concurrently-using-asyncio
    async def stream_events(self):
        logging.info('Starting SFDC Platform Event Monitor.')
        # Setup Streaming Client as a context manager
        async with self.client as c:

            # Add a subscription to the client
            await c.subscribe(self.channel)

            async for message in c:
                await self.process_message(message)



    async def process_message(self, message):
        t = TenantCreateEvent(message['data']['payload'])
        logging.info(f"SFDC Tenant Create Event Received - Self Service Entry Id: {t.ssentry_id}")

        await self.queue.put(t)
