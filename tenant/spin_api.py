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

    return spinnaker_callout(endpoint=endpoint, payload=payload)


def destroy_tenant(tenant_id: str):
    logging.debug('Submitting delete request to Spinnaker...')

    endpoint = config.SymphonyTenantConfig['base_url'] + 'qa_tenant_destroy'
    payload = {
        "secret": config.SymphonyTenantConfig['api_key'],
        "parameters": config.SymphonyTenantConfig['parameters']
    }

    payload['parameters']['tenant'] = tenant_id

    return spinnaker_callout(endpoint=endpoint, payload=payload)


def spinnaker_callout(endpoint: str, payload: dict) -> bool:
    success = False
    submit_enabled = config.SymphonyTenantConfig['submit_enabled']

    if submit_enabled:
        try:
            resp = requests.post(endpoint, data=payload)

            if resp.status_code < 300:
                logging.debug(f"Spinnaker request successful.")
                success = True
            else:
                resp.raise_for_status()

        except Exception as ex:
            logging.error(f'Spinnaker request failed. Error: {ex}')

    else:
        logging.info(f"Spinnaker submission disabled by configuration.")
        success = True

    return success