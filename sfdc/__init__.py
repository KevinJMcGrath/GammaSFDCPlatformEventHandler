import config

from sfdc import api
from sfdc.apex_client import SFClient
from sfdc.events_client import EventsClient

print('Starting Events Client')
PEListenerClient = EventsClient(config.SFDCPlatformConfig)
print('Starting SFDC Client')
SalesforceClient = SFClient(config.SFDCPlatformConfig)

def report_status(ssentry_id: str, tenant_id: str, status: str, message: str=None):
    api.report_status(ssentry_id=ssentry_id, tenant_id=tenant_id, status=status, message=message)

def report_status_pending(ssentry_id: str, tenant_id: str):
    api.report_status(ssentry_id=ssentry_id, tenant_id=tenant_id, status='submitted')

def report_status_in_progress(ssentry_id: str, tenant_id: str):
    api.report_status(ssentry_id=ssentry_id, tenant_id=tenant_id, status='in_progress')

def report_status_complete(ssentry_id: str, tenant_id: str):
    api.report_status(ssentry_id=ssentry_id, tenant_id=tenant_id, status='complete')

def report_status_failed(ssentry_id: str, tenant_id: str):
    api.report_status(ssentry_id=ssentry_id, tenant_id=tenant_id, status='failed')

def report_status_error(ssentry_id: str, tenant_id: str, error_message: str):
    api.report_error(ssentry_id=ssentry_id, tenant_id=tenant_id, err_msg=error_message)