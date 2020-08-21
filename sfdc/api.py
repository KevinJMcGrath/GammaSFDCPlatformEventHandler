from . import SalesforceClient

def report_status(ssentry_id: str, status: str):
    rest_path = '/symphony/sse-status'
    payload = {
        "ssentry_id": ssentry_id,
        "status": status
    }

    SalesforceClient.rest_apex(rest_path=rest_path, method='POST', payload=payload)


def report_error(ssentry_id: str, err_msg: str):
    rest_path = '/symphony/sse-status'
    payload = {
        "ssentry_id": ssentry_id,
        "status": "error",
        "message": err_msg
    }

    SalesforceClient.rest_apex(rest_path=rest_path, method='POST', payload=payload)


def report_system_error(err_msg: str):
    pass