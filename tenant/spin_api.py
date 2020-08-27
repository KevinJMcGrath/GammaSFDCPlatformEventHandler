import logging
import requests

import config

def create_tenant(tenant_id: str=None):
    success = False

    endpoint = config.SymphonyTenantConfig['base_url'] + 'qa_tenant_deploy'
    payload = {
        "secret": config.SymphonyTenantConfig['api_key'],
        "parameters": config.SymphonyTenantConfig['parameters']
    }

    if tenant_id:
        payload['parameters']['tenant'] = tenant_id

    try:
        resp = requests.post(endpoint, data=payload)

        if resp.status_code < 300:
            logging.debug(f"Spinnaker create request successful.")
            success = True
        else:
            resp.raise_for_status()

    except Exception as ex:
        logging.error(ex)
    finally:
        return success


def destroy_tenant(tenant_id: str):
    success = False

    endpoint = config.SymphonyTenantConfig['base_url'] + 'qa_tenant_deploy'
    payload = {
        "secret": config.SymphonyTenantConfig['api_key'],
        "parameters": config.SymphonyTenantConfig['parameters']
    }

    payload['parameters']['tenant'] = tenant_id

    try:
        resp = requests.post(endpoint, data=payload)

        if resp.status_code < 300:
            logging.debug(f"Spinnaker delete request successful.")
            success = True
        else:
            resp.raise_for_status()

    except Exception as ex:
        logging.error(ex)
    finally:
        return success