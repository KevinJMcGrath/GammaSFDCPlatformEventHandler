import db
import errors

# If the tenant_id hasn't been added to the DB or it was attempted previously and failed,
# signal the Id is available for building
def check_tenant_status(tenant_id: str):
    tenant_item = db.DBClient.get_tenant_status(tenant_id)
    if not tenant_item:
        return None
    else:
        return tenant_item['status']



def submit_tenant_build(tenant_id: str):
    tenant_status = check_tenant_status(tenant_id)

    if not tenant_status or tenant_status == 'Failed':
        db.DBClient.insert_tenant_status(tenant_id)
    else:
        raise errors.TenantConflictException(tenant_id, tenant_status)


def update_tenant_status(tenant_id: str, status: db.BuildStatus):
    db.DBClient.update_tenant_status(tenant_id, status)