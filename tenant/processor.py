import logging

import db
import sfdc

from models import tenant as tm
from tenant import spin_api as api

def create_tenant(tenant_event: tm.TenantEvent):
    logging.info(f'Creating new tenant with tenant_id: {tenant_event.tenant_id}')
    # Create new database entry for the inbound tenant
    db.create_new_tenant_entry(tenant_id=tenant_event.tenant_id, ssentry_id=tenant_event.ssentry_id)

    # Submit new tenant to Spinnaker
    success = api.create_tenant(tenant_event.tenant_id)


    if success:
        # Update database entry to in_progress
        db.update_tenant_in_progress(tenant_id=tenant_event.tenant_id)
        # POST update to Salesforce
        sfdc.report_status_in_progress(ssentry_id=tenant_event.ssentry_id, tenant_id=tenant_event.tenant_id)

    else:
        db.update_tenant_failed(tenant_id=tenant_event.tenant_id)
        sfdc.report_status_failed(ssentry_id=tenant_event.ssentry_id, tenant_id=tenant_event.tenant_id)


def status_check(tenant_event: tm.TenantEvent):
    tenant_status_item = db.get_tenant_status(tenant_id=tenant_event.tenant_id)
    ssentry_id = tenant_status_item['ssentry_id']
    tenant_id = tenant_status_item['tenant_id']
    status = tenant_status_item['status']

    sfdc.report_status(ssentry_id=ssentry_id, tenant_id=tenant_id, status=status)


def delete_tenant(tenant_event: tm.TenantEvent):
    logging.info(f'Sunsetting tenant with tenant_id: {tenant_event.tenant_id}')

    success = api.destroy_tenant(tenant_event.tenant_id)

    if success:
        db.update_tenant_status(tenant_id=tenant_event.tenant_id, status='delete_in_progress')
        sfdc.report_status(ssentry_id=tenant_event.ssentry_id, tenant_id=tenant_event.tenant_id, status='delete_in_progress')
    else:
        db.update_tenant_failed(tenant_id=tenant_event.tenant_id)
        sfdc.report_status_failed(ssentry_id=tenant_event.ssentry_id, tenant_id=tenant_event.tenant_id)


def reject_event(tenant_event: tm.TenantEvent, reason: str):
    err_msg = 'unknown'
    if reason == 'invalid_event_auth':
        err_msg = "invalid platform event authorization code."
    elif reason == 'invalid_event_type':
        err_msg = f"invalid platform event type: {tenant_event.type} - tenant_id: {tenant_event.tenant_id}"

    logging.error(f"Event rejected. Reason: {err_msg}")