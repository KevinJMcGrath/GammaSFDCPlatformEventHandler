import logging

import sfdc

def report_status(ssentry_id: str, tenant_id: str, status: str, message: str=None):
    rest_path = 'symphony/sse-status'
    payload = {
        "ssentry_id": ssentry_id,
        "tenant_id": tenant_id,
        "status": status,
        "message": message
    }

    logging.debug(f"Sending status update to SFDC. SSEntryId: {ssentry_id} - status: {status}")
    sfdc.SalesforceClient.rest_apex(rest_path=rest_path, method='POST', payload=payload)


def report_error(ssentry_id: str, tenant_id: str, err_msg: str):
    rest_path = 'symphony/sse-status'
    payload = {
        "ssentry_id": ssentry_id,
        "tenant_id": tenant_id,
        "status": "error",
        "error_message": err_msg
    }

    logging.debug(f"Sending error to SFDC. SSEntryId: {ssentry_id} - error: {err_msg}")
    sfdc.SalesforceClient.rest_apex(rest_path=rest_path, method='POST', payload=payload)
