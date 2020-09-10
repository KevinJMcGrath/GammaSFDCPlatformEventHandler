import logging

from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceExpiredSession


class SFClient:
    def __init__(self, sym_config):
        self.sym_config = sym_config
        self.domain = 'test' if sym_config['sandbox'] else 'login'
        self.client = self.init_client()

    def init_client(self):
        logging.debug('Initializing Salesforce API client...')
        c = Salesforce(username=self.sym_config['username'], password=self.sym_config['password'],
                          security_token=self.sym_config['security_token'], domain=self.domain, client_id='Gamma M.S.')

        api_key = self.sym_config['custom_api_key']
        c.headers['X-SYM-APIKEY'] = api_key

        return c

    def rest_apex(self, rest_path: str, method: str='GET', payload=None):
        retry: bool = False

        try:
            self.client.apexecute(action=rest_path, method=method, data=payload)
        except SalesforceExpiredSession as sfdc_ex:
            retry = True
            logging.error(sfdc_ex)

        except Exception as ex:
            logging.error(ex)

        if retry:
            try:
                logging.info('Attempting to reinitialize the Client and resending the query...')
                self.client = self.init_client()

                self.client.apexecute(action=rest_path, method=method, data=payload)

            except Exception as ex:
                logging.error(ex)
