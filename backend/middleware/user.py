# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import json
import math
import time
from flask import abort, g, request

from config import config
from common import logger
from services.auth_client import AuthClient
from services.jwt_client import Jwt, SecureTokenExpirationSeconds, RefreshTokenExpirationSeconds, ProfileTokenExpirationSeconds

cookieExtension = config['cookie']['extension']
cookieDomain = config['cookie']['domain']

secureCookieName = "devnet_secure_token" + cookieExtension
refreshCookieName = "devnet_secure_refresh_token" + cookieExtension
profileCookieName = "devnet_profile" + cookieExtension


class UserMiddleware:
    def __init__(self, prefix, app):
        self.prefix = prefix
        UserMiddleware.auth_client = AuthClient(config)

        def before():
            return self.before_request()
        app.before_request(before)
        app.after_request(UserMiddleware.after_request)

    @staticmethod
    def refresh_token(token):
        try:
            refresh_claims = Jwt.verify(token)
            profile = UserMiddleware.auth_client.get_profile_by_id(refresh_claims['profileID'])
            if not profile:
                logger.error("Could not get profile: '{profile}'!".format(profile=refresh_claims))
                return None

            email = AuthClient.get_email_by_provider(profile, refresh_claims['iss'])
            if not email:
                logger.error("Could not get email from '{profile}'!".format(profile=refresh_claims))
                return None

            account = UserMiddleware.auth_client.get_account_by_id(email + str(refresh_claims['iss']))
            if not account:
                logger.error("Could not get account: '{email}{iss}'!".format(email=email, iss=refresh_claims['iss']))
                return None

            secure_token = Jwt.create_secure_token(account, SecureTokenExpirationSeconds)
            refresh_token = Jwt.create_secure_refresh_token(account, RefreshTokenExpirationSeconds)
            profile_token = Jwt.create_profile_token(account, profile, ProfileTokenExpirationSeconds)

            now = math.floor(time.time())
            g.tokens = [
                (secureCookieName, secure_token, SecureTokenExpirationSeconds + now, True),
                (refreshCookieName, refresh_token, RefreshTokenExpirationSeconds + now, True),
                (profileCookieName, profile_token, ProfileTokenExpirationSeconds + now, False)
            ]

            return secure_token
        except Exception as e:
            logger.error("Could not get refresh claims from JWT: '{message}'!".format(message=str(e)))
            return None

    @staticmethod
    def parse_jwt(token):
        try:
            g.user_claims = Jwt.verify(token)
            perms = g.user_claims['perms']
            if perms and len(perms):
                logger.debug("Authorized as user with permissions: {perms}".format(perms=json.dumps(perms)))
            else:
                logger.debug("Authorized as user with NO permissions!")
            return True
        except Exception as e:
            logger.error("Could not get claims from JWT: '{message}'!".format(message=str(e)))
            return False

    def before_request(self):
        if request.method == "OPTIONS" or not request.path.startswith(self.prefix):
            return

        logger.debug("Enter user middleware for request: {method} {url}".format(method=request.method, url=request.path))
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        elif secureCookieName in request.cookies:
            token = request.cookies.get(secureCookieName)
        else:
            logger.debug("No authorization header, request will be anonymous")
            return

        if token and UserMiddleware.parse_jwt(token):
            return

        refresh_token = request.cookies.get(refreshCookieName)
        if refresh_token:
            token = UserMiddleware.refresh_token(refresh_token)
            if token and UserMiddleware.parse_jwt(token):
                return
            else:
                abort(401)

    @staticmethod
    def after_request(response):
        for (name, token, expires, httpOnly) in g.get('tokens', []):
            response.set_cookie(name, token, path="/", domain=cookieDomain, secure=True,
                                expires=expires * 1000, httponly=httpOnly)
        return response
