import asyncio
import logging

from datetime import datetime, timezone, timedelta

import db
import sfdc

# Build Monitor will query for a list of tenant_ids that are 'InProgress' and poll
# the Spinnaker endpoint to check for completion
async def monitor_tenants():
    while True:
        await asyncio.sleep(30)

        results = db.get_pending_tenants()

        for tenant in results:
            curr_dt = datetime.now(tz=timezone.utc)
            created_datetime = db.utility.get_created_datetime(tenant)

            db_id = tenant['_id']
            # tenant_id = tenant['tenant_id']
            ssentry_id = tenant['ssentry_id']

            if created_datetime + timedelta(minutes=2) <= curr_dt:
                logging.info(f'Tenant is complete - notifying Salesforce. SSEntry_Id: {ssentry_id}')
                db.update_tenant_status_by_id(db_id=db_id, status='complete')

                sfdc.report_status_complete(ssentry_id=ssentry_id)
