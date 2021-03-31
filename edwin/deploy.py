from edwin import kube, security, symphony

def execute_edwin_deploy(tenant_id: str, company_name: str):
    bot_username = 'mtadminbot'
    deployment_name = f'{bot_username}-{tenant_id}'

    # Generate RSA4096 keypair and return pair in PEM format base64 encoded
    pub_key_64, priv_key_64 = security.generate_rsa_key_pair()

    bot_config_64 = symphony.create_bot_config(tenant_id)

    kube_secret = kube.create_secret(secret_name=deployment_name, bot_config_64=bot_config_64,
                                     private_key_64=priv_key_64)


