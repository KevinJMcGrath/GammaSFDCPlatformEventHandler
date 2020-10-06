import logging
import requests

import config

from models import tenant as tm

def create_tenant(tenant_event: tm.TenantEvent) -> (bool, str):
    try:
        endpoint = config.SymphonyTenantConfig['base_url'] + config.SymphonyTenantConfig['create_tenant_endpoint']
        payload = {
            "secret": config.SymphonyTenantConfig['api_key'],
            "parameters": config.SymphonyTenantConfig['parameters']
        }

        # if tenant_id:
        #     payload['parameters']['tenant'] = tenant_id

        payload['parameters']['tenant_name'] = tenant_event.company_name
        payload['parameters']['tenant_admin_email'] = tenant_event.email
        payload['parameters']['tenant_admin_first'] = tenant_event.firstname
        payload['parameters']['tenant_admin_last'] = tenant_event.lastname

        return spinnaker_callout(endpoint=endpoint, payload=payload)

    except KeyError as ex_key:
        logging.error('Missing parameter from event payload. ')
        logging.exception(ex_key)
        return False, ''


def destroy_tenant(tenant_id: str):
    logging.debug('Submitting delete request to Spinnaker...')

    endpoint = config.SymphonyTenantConfig['base_url'] + config.SymphonyTenantConfig['destroy_tenant_endpoint']
    payload = {
        "secret": config.SymphonyTenantConfig['api_key'],
        "parameters": config.SymphonyTenantConfig['parameters']
    }

    payload['parameters']['tenant'] = tenant_id

    return spinnaker_callout(endpoint=endpoint, payload=payload)


def spinnaker_callout(endpoint: str, payload: dict) -> (bool, str):
    success = False
    event_id = ''
    submit_enabled = config.SymphonyTenantConfig['submit_enabled']

    if submit_enabled:
        try:
            resp = requests.post(endpoint, json=payload)

            if resp.status_code < 300:
                logging.debug(f"Spinnaker request successful.")
                success = True
                event_id = resp.json()['eventId']
            else:
                resp.raise_for_status()
        except requests.exceptions.HTTPError as http_ex:
            logging.error('Spinnaker HTTP Error')
            logging.exception(http_ex)
            logging.error(http_ex.response.text)
        except Exception as ex:
            logging.error(f'Spinnaker request failed. Error: {ex}')

    else:
        logging.info(f"Spinnaker submission disabled by configuration.")
        success = True

    return success, event_id