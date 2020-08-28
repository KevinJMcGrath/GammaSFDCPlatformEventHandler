import config

from models import tenant as tm

# TODO: encrypt auth code with datetime
def check_platform_event_authorized(tenant_event: tm.TenantEvent):
    auth_code = config.SFDCPlatformConfig['event_auth_code']

    return tenant_event.auth_code == auth_code