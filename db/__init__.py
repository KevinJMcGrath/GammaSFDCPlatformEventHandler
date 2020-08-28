from db.client import MongoClient


DBClient = MongoClient.from_config()
DBClient.test_conn()


def create_new_tenant_entry(tenant_id: str, ssentry_id: str):
    DBClient.insert_new_tenant(tenant_id=tenant_id, ssentry_id=ssentry_id)

def update_tenant_status(tenant_id: str, status: str):
    DBClient.update_tenant_status(tenant_id=tenant_id, status=status)

def update_tenant_in_progress(tenant_id: str):
    DBClient.update_tenant_status(tenant_id=tenant_id, status='in_progress')

def update_tenant_failed(tenant_id: str):
    DBClient.update_tenant_status(tenant_id=tenant_id, status='failed')

def update_tenant_complete(tenant_id: str):
    DBClient.update_tenant_status(tenant_id=tenant_id, status='complete')

def get_tenant_status(tenant_id: str):
    return DBClient.get_tenant_status(tenant_id=tenant_id)
