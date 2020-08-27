import asyncio

from models import tenant
from tenant import processor

async def process_events(async_queue: asyncio.Queue):
    while True:
        tenant_event = await async_queue.get()

        if isinstance(tenant_event, tenant.TenantCreateEvent):
            pass


def process_event_create_tenant(tenant_event: tenant.TenantCreateEvent):
    processor.create_tenant(tenant_event=tenant_event)
