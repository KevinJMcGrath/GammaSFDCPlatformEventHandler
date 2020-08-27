import config


from . import api
from .apex_client import SFClient
from .events_client import EventsClient


PEListenerClient = EventsClient(config.SFDCPlatformConfig)
SalesforceClient = SFClient(config.SFDCPlatformConfig)

def report_status_pending(ss_entry_id: str):
    api.report_status(ssentry_id=ss_entry_id, status='submitted')

def report_status_in_progress(ss_entry_id: str):
    api.report_status(ssentry_id=ss_entry_id, status='in_progress')

def report_status_complete(ss_entry_id: str):
    api.report_status(ssentry_id=ss_entry_id, status='complete')

def report_status_failed(ss_entry_id: str):
    api.report_status(ssentry_id=ss_entry_id, status='failed')