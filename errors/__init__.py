class TenantConflictException(Exception):
    def __init__(self, tenant_id: str, status: str):
        super().__init__(f"Attempt to build tenant with id {tenant_id} failed. Tenant status: {status}")


class TenantFailedException(Exception):
    def __init__(self, tenant_id: str):
        super().__init__(f"Tenant status check for tenant id: {tenant_id} returned FAILED.")