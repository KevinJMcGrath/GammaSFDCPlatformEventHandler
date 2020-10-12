import logging

import config

from models import tenant as tm
from sfdc import api
from sfdc.apex_client import SFClient
from sfdc.events_client import EventsClient


print('Starting Events Client')
PEListenerClient = EventsClient(config.SFDCPlatformConfig)
print('Starting SFDC Client')
SalesforceClient = SFClient(config.SFDCPlatformConfig)



def report_status_pending(te:tm.TenantEvent):
    api.report_status(ssentry_id=te.ssentry_id, status='submitted')

def report_status_in_progress(te: tm.TenantEvent):
    api.report_status(ssentry_id=te.ssentry_id, status='in_progress', company_name=te.company_name,
                      admin_email=te.email, admin_firstname=te.firstname, admin_lastname=te.lastname)

def report_status_failed(te:tm.TenantEvent):
    api.report_status(ssentry_id=te.ssentry_id, status='failed')

def report_status_error(ssentry_id: str, error_message: str):
    api.report_error(ssentry_id=ssentry_id, err_msg=error_message)

def report_status_proof_of_life(app_version_id: str):
    api.report_status(ssentry_id=app_version_id, status='system_check')

# Non-Tenant_Event status updates
def report_status(ssentry_id: str, status: str, message: str=None):
    api.report_status(ssentry_id=ssentry_id, status=status, message=message)

def report_status_complete(ssentry_id: str):
    if config.SymphonyTenantConfig['finalize_enabled']:
        api.report_status(ssentry_id=ssentry_id, status='complete')
    else:
        logging.info('Finalize tenant skipped. Finalize disabled in config.')