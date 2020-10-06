import db.utility as utility

from db.client import MongoClient


DBClient = MongoClient.from_config()
DBClient.test_conn()

# Do I need to log the mt_event_id?
def create_new_tenant_entry(ssentry_id: str):
    DBClient.insert_new_tenant(ssentry_id=ssentry_id)

def update_tenant_status(ssentry_id: str, status: str):
    DBClient.update_tenant_status_by_ssentry_id(ssentry_id=ssentry_id, status=status)

def update_tenant_status_by_id(db_id, status: str):
    DBClient.update_tenant_status_by_id(db_id=db_id, status=status)

def update_tenant_in_progress(ssentry_id: str):
    DBClient.update_tenant_status_by_ssentry_id(ssentry_id=ssentry_id, status='in_progress')

def update_tenant_failed(ssentry_id: str):
    DBClient.update_tenant_status_by_ssentry_id(ssentry_id=ssentry_id, status='failed')

def update_tenant_complete(ssentry_id: str):
    DBClient.update_tenant_status_by_ssentry_id(ssentry_id=ssentry_id, status='complete')

def update_tenant_mt_event_id(ssentry_id: str, mt_event_id: str):
    DBClient.update_tenant_event_id_by_ssentry_id(ssentry_id=ssentry_id, mt_event_id=mt_event_id)

def get_tenant_status(ssentry_id: str):
    return DBClient.get_tenant_status_by_ssentry_id(ssentry_id=ssentry_id)

def get_pending_tenants():
    return DBClient.get_pending_tenants()
