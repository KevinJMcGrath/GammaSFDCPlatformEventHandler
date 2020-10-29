import aiohttp
import asyncio
import logging
import requests

from requests_toolbelt import MultipartEncoder

import config

from bot import auth
from bot import errors

class BotClient:
    def __init__(self):
        self.df_create_ep = f"{config.BotConfig['auth_host']}/agent/v4/datafeed/create"
        self.datafeed_id = ''

        self.auth_client = auth.AuthClient()
        self.loop_control = True

        self.async_session = aiohttp.ClientSession()

    def get_df_read_ep(self):
        return f"{config.BotConfig['auth_host']}/agent/v4/datafeed/{self.datafeed_id}/read"

    async def start_datafeed(self):
        logging.info('Initializing Gamma Bot datafeed...')
        resp = await self.sym_rest(self.df_create_ep, 'POST')

        if resp:
            self.datafeed_id = resp['id']
        else:
            logging.error('Unable to start datafeed')

    async def read_datafeed(self):
        if not self.datafeed_id:
            await self.start_datafeed()

        if self.datafeed_id:
            ep = self.get_df_read_ep()

            return await self.sym_rest_async(ep)
        else:
            logging.error('Missing datafeed id')
            raise errors.MissingDatafeedIdException

    async def sym_rest_async(self, endpoint: str, method: str='GET', body=None):
        if not self.auth_client.is_valid():
            await self.auth_client.authenticate()


        async with self.async_session.request(method=method, url=endpoint, json=body,
                                              headers=self.auth_client.get_headers()) as r:
            try:
                resp_json = await r.json()

                if r.status // 100 == 2:
                    logging.debug(f'aiohttp success - {r.status} - {r.real_url} - {resp_json}')
                    return resp_json
                else:
                    r.raise_for_status()

            except aiohttp.ClientResponseError as resp_ex:
                logging.error(f'aiohttp Response Error - status: {resp_ex.status} - message: {resp_ex.message}')
                logging.exception(resp_ex)
            except aiohttp.ClientError as c_ex:
                logging.error('aiohttp Client Error')
                logging.exception(c_ex)
            except Exception as ex:
                logging.error('Bot Client General Error')
                logging.exception(ex)

    async def sym_rest(self, endpoint: str, method: str='GET', body=None):
        if not self.auth_client.is_valid():
            await self.auth_client.authenticate()

        try:
            resp = None
            if method == 'GET':
                resp = requests.get(endpoint, headers=self.auth_client.get_headers())
            elif method == 'POST':
                resp = requests.post(endpoint, data=body, headers=self.auth_client.get_headers())
            elif method == 'POSTV2':
                encoder = MultipartEncoder(fields=body)
                h = self.auth_client.get_headers(encoder.content_type)

                resp = requests.post(endpoint, data=encoder, headers=h)
            else:
                raise errors.MethodNotImplementedException

            if resp.status_code // 100 == 2:
                return resp.json()
            else:
                resp.raise_for_status()

        except requests.exceptions.HTTPError as h_ex:
            logging.error('Bot Client HTTP Error')
            logging.exception(h_ex)
        except requests.exceptions.RequestException as r_ex:
            logging.error('Bot Client Requests Error')
            logging.exception(r_ex)
        except Exception as ex:
            logging.error('Bot Client General Error')
            logging.exception(ex)

        return None

