import jwt

from datetime import datetime, timedelta


def generate_jwt(bot_username: str, private_key_path: str):
    header = {
        "typ": "JWT",
        "alg": "RS512"
    }

    # Make sure you're using datetime.utcnow() and not datetime.now()
    payload = {
        "sub": bot_username,
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }

    with open(private_key_path, 'r') as keyfile:
        private_key = keyfile.read()

    return jwt.encode(payload, private_key, algorithm='RS512', headers=header)