import asyncio

from models import tenant
from tenant import processor

async def process_events(async_queue: asyncio.Queue):
    while True:
        tenant_event: tenant.TenantEvent = await async_queue.get()

        if tenant_event.type == 'create':
            processor.create_tenant(tenant_event=tenant_event)
        elif tenant_event.type == 'status':
            processor.status_check(tenant_event)
        elif tenant_event.type == 'delete':
            processor.delete_tenant(tenant_event)
