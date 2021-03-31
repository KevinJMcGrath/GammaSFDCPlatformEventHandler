from jira import JIRA
from pathlib import Path

import config

class JIRAClient:
    def __init__(self):
        self.client = None

        self.load_config()

    def load_config(self):
        server = config.JIRAConfig['server']
        # uname = config.JIRAConfig['username']
        # token = config.JIRAConfig['api_token']

        access_token = config.JIRAConfig['access_token']
        access_token_secret = config.JIRAConfig['access_token_secret']
        consumer_key = config.JIRAConfig['consumer_key']
        private_key_path = Path(config.JIRAConfig['private_key_path'])

        with open(private_key_path, 'r') as priv_key_file:
            key_cert_data = priv_key_file.read()

        oauth_dict = {
            "access_token": access_token,
            "access_token_secret": access_token_secret,
            "consumer_key": consumer_key,
            "key_cert": key_cert_data
        }

        self.client = JIRA(server=server, oauth=oauth_dict)