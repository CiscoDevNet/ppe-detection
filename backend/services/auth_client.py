# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


from services.blob_client import BlobClient


userAccountBlobTypeName = "useraccount"
userProfileBlobTypeName = "userprofile"


class AuthClient:
    def __init__(self, config):
        self.blob_client = BlobClient(config)

    def get_profile_by_id(self, profile_id):
        profile = self.blob_client.get_blob(userProfileBlobTypeName, profile_id)
        if profile:
            return profile.data
        return None

    def get_account_by_id(self, account_id):
        account = self.blob_client.get_blob(userAccountBlobTypeName, account_id)
        if account:
            return account.data
        return None

    @staticmethod
    def get_email_by_provider(profile, issuer):
        for account in profile['accounts']:
            if account.endswith(issuer):
                return account[:(len(account)-len(issuer))]
        return None
