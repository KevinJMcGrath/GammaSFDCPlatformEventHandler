import logging

from simple_salesforce import Salesforce


class SFClient:
    def __init__(self, sym_config):
        self.domain = 'test' if sym_config['sandbox'] else 'login'
        self.client = self.init_client(sym_config)

    def init_client(self, sym_config):
        logging.debug('Initializing Salesforce API client...')
        c = Salesforce(username=sym_config['username'], password=sym_config['password'],
                          security_token=sym_config['security_token'], domain=self.domain)

        api_key = sym_config['custom_api_key']
        c.headers['X-SYM-APIKEY'] = api_key

        return c


    def rest_apex(self, rest_path: str, method: str='GET', payload=None):
        try:
            self.client.apexecute(action=rest_path, method=method, data=payload)
        except Exception as ex:
            logging.error(ex)
