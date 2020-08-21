from . import SalesforceClient

def report_status(ssentry_id: str, status: str):
    rest_path = '/symphony/sse-status'
    payload = {
        "ssentry_id": ssentry_id,
        "status": status
    }

    SalesforceClient.rest_apex(rest_path=rest_path, method='POST', payload=payload)
