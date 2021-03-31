import asyncio
import logging
import requests


from datetime import datetime, timedelta
from pathlib import Path

import config
import bot.jwt_gen as jwt

class AuthClient:
    def __init__(self):
        self.username = config.BotConfig['bot_username']
        self.session_ep = f"{config.BotConfig['auth_host']}/login/pubkey/authenticate"
        self.km_ep = f"{config.BotConfig['auth_host']}/relay/pubkey/authenticate"
        self.private_key_path = Path(f"{config.BotConfig['secrets_folder']}/{config.BotConfig['private_key_filename']}")

        self.session_token = ''
        self.km_token = ''
        self.valid_until = None
        self.backoff_counter = 0

    def get_headers(self, content_type: str='application/json'):
        return {
            "sessionToken": self.session_token,
            "keyManagerToken": self.km_token,
            "Content-Type": content_type,
            "User-Agent": "GammaBot (Kevin McGrath - BizOps - kevin.mcgrath@symphony.com)"
        }

    async def authenticate(self):
        logging.info('Authenticating Gamma Bot...')

        self.session_token = ''
        self.km_token = ''
        self.valid_until = None

        backoff_seconds = 0
        if self.backoff_counter != 0:
            backoff_seconds = 2**self.backoff_counter

            if backoff_seconds > 900:
                backoff_seconds = 900

            logging.info(f'Waiting {backoff_seconds}s before attempting re-authentication...')
            await asyncio.sleep(backoff_seconds)

        jwt_payload = jwt.generate_jwt(self.username, self.private_key_path)


        self.session_token = get_auth_token(self.session_ep, jwt_payload)

        if self.session_token:
            self.backoff_counter = 0
            self.km_token = get_auth_token(self.km_ep, jwt_payload)
            self.valid_until = datetime.now() + timedelta(days=7)

            logging.info(f'Session valid until {self.valid_until}' )

        else:
            logging.error(f'Authentication failed ({self.backoff_counter + 1} attempts) . Trying again in {backoff_seconds}s')

            self.backoff_counter += 1


    def is_valid(self):
        is_v = self.session_token and self.valid_until and datetime.now() <= self.valid_until
        logging.debug(f'Gamma Bot session is {"valid" if is_v else "invalid"}')
        return is_v

    def invalidate(self):
        self.session_token = self.km_token = ''
        self.valid_until = None

def get_auth_token(endpoint: str, jwt_encoded):
    try:
        payload = {
            "token": jwt_encoded
        }

        response = requests.post(endpoint, json=payload)

        if response.status_code == 200:
            resp_json = response.json()
            return resp_json['token']

    except requests.exceptions.HTTPError as httpex:
        print(httpex)

    except requests.exceptions.RequestException as connex:
        print(connex)

    except Exception as ex:
        print(ex)

    return ''