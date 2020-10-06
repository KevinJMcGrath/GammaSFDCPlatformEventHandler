import logging

import sfdc


def report_status(ssentry_id: str, status: str, **kwargs):
    rest_path = 'symphony/sse-status'
    payload = {
        "ssentry_id": ssentry_id,
        "status": status,
        "message":  kwargs.get('message', ''),
        "tenant_id": kwargs.get('tenant_id', ''),
        "company_name": kwargs.get('company_name', ''),
        "admin_email": kwargs.get('admin_email', ''),
        "admin_firstname": kwargs.get('admin_firstname', ''),
        "admin_lastname": kwargs.get('admin_lastname', '')
    }


    logging.debug(f"Sending status update to SFDC. SSEntryId: {ssentry_id} - status: {status}")
    sfdc.SalesforceClient.rest_apex(rest_path=rest_path, method='POST', payload=payload)


def report_error(ssentry_id: str, err_msg: str):
    rest_path = 'symphony/sse-status'
    payload = {
        "ssentry_id": ssentry_id,
        "status": "error",
        "error_message": err_msg
    }

    logging.debug(f"Sending error to SFDC. SSEntryId: {ssentry_id} - error: {err_msg}")
    sfdc.SalesforceClient.rest_apex(rest_path=rest_path, method='POST', payload=payload)
