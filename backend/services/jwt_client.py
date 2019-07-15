# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


import base64
import hvac
import jwt
import math
import time
import uuid
from config import config

SecureTokenExpirationSeconds = 20 * 60  # 20 minutes
RefreshTokenExpirationSeconds = 365 * 24 * 60 * 60  # 1 year
ProfileTokenExpirationSeconds = 24 * 60 * 60  # 1 day
InternalExpirationSeconds = 24 * 60 * 60  # 1 day

secretPath = "secret/jwt"

defaultPerms = [
    {
        "company": "*",
        "domain": "*",
        "role": "*",
        "user": "*"
    }
]

defaultAbac = {
    'read': defaultPerms,
    'write': defaultPerms,
    'delete': defaultPerms
}


class Jwt:
    @staticmethod
    def init_standard_claims(claims, provider, expiry_seconds):
        now = math.floor(time.time())
        claims["jti"] = str(uuid.uuid1())
        claims['iat'] = now - 300
        claims['exp'] = now + expiry_seconds
        claims['iss'] = provider or 'internal'

    @staticmethod
    def get_jwt_secret():
        if config['vault']['jwtSecretValue']:
            return config['vault']['jwtSecretValue']
        else:
            client = hvac.Client(url=config['vault']['endpoint'], token=config['vault']['token'])
            data = client.read('secret/jwt')
            return data['data']['value']

    @staticmethod
    def verify(token):
        secret = Jwt.get_jwt_secret()
        return jwt.decode(token, base64.b64decode(secret))
        
    @staticmethod
    def get_user_token(user_claims, provider):
        Jwt.init_standard_claims(user_claims, provider, InternalExpirationSeconds)
        secret = Jwt.get_jwt_secret()
        d = jwt.encode(user_claims, base64.b64decode(secret))
        return str(d, 'UTF-8')

    @staticmethod
    def get_sudo_token():
        return Jwt.get_user_token({"perms": defaultPerms}, None)

    @staticmethod
    def create_secure_token(account, expires):
        user_claims = {
            "profileID": account['profileID'],
            "perms": account['permissions'],
            "accesslevel": account['accesslevel']
        }
        Jwt.init_standard_claims(user_claims, account['provider'], expires)
        secret = Jwt.get_jwt_secret()
        d = jwt.encode(user_claims, base64.b64decode(secret))
        return str(d, 'UTF-8')

    @staticmethod
    def create_secure_refresh_token(account, expires):
        refresh_claims = {
            "profileID": account['profileID']
        }
        Jwt.init_standard_claims(refresh_claims, account['provider'], expires)
        secret = Jwt.get_jwt_secret()
        d = jwt.encode(refresh_claims, base64.b64decode(secret))
        return str(d, 'UTF-8')

    @staticmethod
    def create_profile_token(account, profile, expires):
        profile_claims = {
            "profileID": profile['id'],
            "firstName": profile['user']['firstName'],
            "lastName": profile['user']['lastName'],
            "displayName": profile['user']['displayName']
        }
        Jwt.init_standard_claims(profile_claims, account['provider'], expires)
        secret = Jwt.get_jwt_secret()
        d = jwt.encode(profile_claims, base64.b64decode(secret))
        return str(d, 'UTF-8')
