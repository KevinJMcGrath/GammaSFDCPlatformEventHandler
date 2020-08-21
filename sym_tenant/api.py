import logging
import requests

import config

def create_tenant(tenant_id: str=None):
    endpoint = config.SymphonyTenantConfig['base_url'] + 'qa_tenant_deploy'

    payload = {
        "secret": config.SymphonyTenantConfig['api_key'],
        "parameters": config.SymphonyTenantConfig['parameters']
    }

    if tenant_id:
        payload['parameters']['tenant'] = tenant_id

    try:
        resp = requests.post(endpoint, data=payload)

        if resp.status_code > 299:
            resp.raise_for_status()

    except Exception as ex:
        logging.error(ex)


def destroy_tenant(tenant_id: str):
    endpoint = config.SymphonyTenantConfig['base_url'] + 'qa_tenant_deploy'

    payload = {
        "secret": config.SymphonyTenantConfig['api_key'],
        "parameters": config.SymphonyTenantConfig['parameters']
    }

    payload['parameters']['tenant'] = tenant_id

    try:
        resp = requests.post(endpoint, data=payload)

        if resp.status_code > 299:
            resp.raise_for_status()

    except Exception as ex:
        logging.error(ex)