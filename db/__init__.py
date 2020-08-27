from db.client import MongoClient
from db.utility import BuildStatus


DBClient = MongoClient.from_config()


def create_new_tenant_entry(tenant_id: str):
    DBClient.insert_new_tenant(tenant_id=tenant_id)

def update_tenant_in_progress(tenant_id: str):
    DBClient.update_tenant_status(tenant_id=tenant_id, status=BuildStatus.InProgress)

def update_tenant_failed(tenant_id: str):
    DBClient.update_tenant_status(tenant_id=tenant_id, status=BuildStatus.Failed)

def update_tenant_complete(tenant_id: str):
    DBClient.update_tenant_status(tenant_id=tenant_id, status=BuildStatus.Complete)
