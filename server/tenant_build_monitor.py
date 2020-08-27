# Build Monitor will query for a list of tenant_ids that are 'InProgress' and poll
# the Spinnaker endpoint to check for completion

import asyncio

async def monitor_builds():
    while True:
        await asyncio.sleep(1)