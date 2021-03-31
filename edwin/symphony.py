import base64
import jsonpickle

def create_bot_config(tenant_id: str):
    url = f'{tenant_id}.p.symphony.com'

    bot_config = {
        "sessionAuthHost": url,
        "sessionAuthPort": 443,
        "keyAuthHost": url,
        "keyAuthPort": 443,
        "podHost": url,
        "podPort": 443,
        "agentHost": url,
        "agentPort": 443,
        "botUsername": "mtadminbot",
        "botEmailAddress": f"mtadminbot@{url}",
        "authType": "rsa",
        "botPrivateKeyPath": "/app/config/",
        "botPrivateKeyName": "private.pem",
    }

    json_str = jsonpickle.encode(bot_config, unpicklable=False)

    return base64.b64encode(json_str.encode('utf-8'))