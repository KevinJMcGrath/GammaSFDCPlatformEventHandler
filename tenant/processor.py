import logging

import db
import sfdc

from models import tenant as tm
from tenant import spin_api as api

def create_tenant(tenant_event: tm.TenantEvent):
    logging.info(f'Creating new tenant with tenant_id: {tenant_event.tenant_id}')
    # Create new database entry for the inbound tenant
    db.create_new_tenant_entry(tenant_event.tenant_id)

    # Submit new tenant to Spinnaker
    # success = api.create_tenant(tenant_event.tenant_id)
    success = True

    if success:
        # Update database entry to InProgress
        db.update_tenant_in_progress(tenant_id=tenant_event.tenant_id)
        # POST update to Salesforce
        sfdc.report_status_in_progress(ss_entry_id=tenant_event.ssentry_id)

    else:
        db.update_tenant_failed(tenant_id=tenant_event.tenant_id)
        sfdc.report_status_failed(ss_entry_id=tenant_event.ssentry_id)


def status_check(tenant_event: tm.TenantEvent):
    pass


def delete_tenant(tenant_event: tm.TenantEvent):
    # Delete tenant probably requires a monitoring queue too,
    # the delete is not instantaneous and can potentially fail, which
    # might cause a conflict

    pass

