import asyncio
import logging

import security

from models import tenant
from tenant import processor

async def process_events(async_queue: asyncio.Queue):
    while True:
        tenant_event: tenant.TenantEvent = await async_queue.get()

        logging.debug('Event item retreived from queue.')
        if security.platform_auth.check_platform_event_authorized(tenant_event):
            if tenant_event.type == 'create':
                processor.create_tenant(tenant_event=tenant_event)
            elif tenant_event.type == 'status':
                processor.status_check(tenant_event)
            elif tenant_event.type == 'delete':
                processor.delete_tenant(tenant_event)
            elif tenant_event.type == 'system_check':
                processor.send_proof_of_life()
            elif tenant_event.type == 'list_pending':
                processor.event_type_not_implemented(tenant_event)
            else:
                processor.reject_event(tenant_event, reason="invalid_event_type")
        else:
            processor.reject_event(tenant_event, reason="invalid_event_auth")

        async_queue.task_done()
        logging.debug('Event item fully processed.')