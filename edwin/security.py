import base64
import logging

from Crypto.PublicKey import RSA

def generate_rsa_key_pair():
    logging.info('Generating RSA keypair...')
    keypair = RSA.generate(4096)

    public_key = keypair.publickey()
    public_key_pem = public_key.exportKey()
    private_key_pem = keypair.exportKey()

    public_key_pem_64 = base64.b64encode(public_key_pem)
    private_key_pem_64 = base64.b64encode(private_key_pem)

    return public_key_pem_64, private_key_pem_64