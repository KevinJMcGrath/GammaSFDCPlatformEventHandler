import asyncio
import logging
import lxml

from bs4 import BeautifulSoup

import bot
import config


from bot import errors
from models.symphony import Message
from tenant import finalize_tenant as ft


accept_from_stream_id = config.BotConfig['stream_id']

async def monitor_tenant_symphony_stream():
    await asyncio.sleep(1)

    while True:
        try:

            messages = await bot.client.read_datafeed()

            if messages:
                for msg in messages:
                    inbound = Message(msg)

                    if inbound.message_type != 'MESSAGESENT':
                        continue

                    if inbound.stream.stream_id != accept_from_stream_id:
                        continue

                    logging.info('Gamma Notification Received')
                    p_msg = parse_message(inbound.message.message_ml)

                    if p_msg and p_msg['id']:
                        t_id = p_msg['id']
                        t_email = p_msg['email']
                        t_password = p_msg['password']

                        logging.info(f'Tenant complete - tenant_id: {t_id} - admin_email: {t_email}')

                        ft.finalize(t_id, t_email, t_password)


        except errors.MissingDatafeedIdException as df_ex:
            logging.error('Datafeed Id Missing')
            logging.exception(df_ex)
        except Exception as ex:
            logging.exception(ex)
            raise ex

def parse_message(msg):
    tenant_id = ''
    tenant_email = ''
    tenant_password = ''

    if not msg:
        return None

    soup = BeautifulSoup(msg, 'lxml')

    is_new_tenant = False
    for tag in soup.find_all('span'):
        if tag.text and tag.text.lower() == '#new-tenant':
            is_new_tenant = True
            break

    if is_new_tenant:
        for tag in soup.select(".cardBody > div"):
            line_s = tag.text.split(':')

            if line_s[0].lower() == 'tenant id':
                tenant_id = line_s[1].strip()
            elif line_s[0].lower() == 'tenant admin email':
                tenant_email = line_s[1].strip()
            elif line_s[0].lower() == 'tenant password':
                tenant_password = line_s[1].strip()

        return {
            "id": tenant_id,
            "email": tenant_email,
            "password": tenant_password
        }



    return None