import db.utility as utility

from db.client import MongoClient
from models import tenant as tm


DBClient = MongoClient.from_config()
DBClient.test_conn()

# Do I need to log the mt_event_id?
def create_new_tenant_entry(t: tm.TenantEvent):
    DBClient.insert_new_tenant(ssentry_id=t.ssentry_id, admin_email=t.email, company_name=t.company_name,
                               admin_fname=t.firstname, admin_lname=t.lastname)

def update_tenant_status(t: tm.TenantEvent, status: str):
    DBClient.update_tenant_status_by_ssentry_id(ssentry_id=t.ssentry_id, status=status)

def update_tenant_status_by_id(db_id, status: str):
    DBClient.update_tenant_status_by_id(db_id=db_id, status=status)

def update_tenant_in_progress(t: tm.TenantEvent):
    DBClient.update_tenant_status_by_ssentry_id(ssentry_id=t.ssentry_id, status='in_progress')

def update_tenant_failed(t: tm.TenantEvent):
    DBClient.update_tenant_status_by_ssentry_id(ssentry_id=t.ssentry_id, status='failed')

def update_tenant_complete_by_ssentry_id(ssentry_id: str):
    DBClient.update_tenant_status_by_ssentry_id(ssentry_id=ssentry_id, status='complete')

def get_tenant_status(t: tm.TenantEvent):
    return DBClient.get_tenant_status_by_ssentry_id(ssentry_id=t.ssentry_id)

def get_tenant_by_admin_email(admin_email: str):
    return DBClient.get_tenant_status_by_admin_email(admin_email)

def get_pending_tenants():
    return DBClient.get_pending_tenants()
