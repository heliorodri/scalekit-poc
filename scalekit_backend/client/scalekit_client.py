from scalekit.client import ScalekitClient
from scalekit.common.scalekit import AuthorizationUrlOptions, CodeAuthenticationOptions
from dotenv import load_dotenv
import os

from scalekit.users import GetUserResponse


load_dotenv(dotenv_path='.env')

SCALEKIT_ENVIRONMENT_URL = os.environ.get('SCALEKIT_ENVIRONMENT_URL')
SCALEKIT_CLIENT_ID = os.environ.get('SCALEKIT_CLIENT_ID')
SCALEKIT_CLIENT_SECRET = os.environ.get('SCALEKIT_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
ORGANIZATION_ID = os.environ.get('SCALEKIT_ORG_ID')

class ScClient(ScalekitClient):
    def __init__(self):
        if not SCALEKIT_ENVIRONMENT_URL or not SCALEKIT_CLIENT_ID or not SCALEKIT_CLIENT_SECRET or not REDIRECT_URI:
            raise ValueError("SCALEKIT_ENVIRONMENT_URL, SCALEKIT_CLIENT_ID, and SCALEKIT_CLIENT_SECRET must be set")

        super().__init__(
            SCALEKIT_ENVIRONMENT_URL,
            SCALEKIT_CLIENT_ID,
            SCALEKIT_CLIENT_SECRET
        )

    def authorization_url(self, code: str):
        return f'{self.get_authorization_url(str(REDIRECT_URI), self.authorization_options())}?code={code}'

    def authenticate_using_code(self, code: str):
        if not code:
            raise ValueError("Code is required")
        
        return super().authenticate_with_code(code, str(REDIRECT_URI), self.code_authentication_options())

    def authorization_options(self):
        options = AuthorizationUrlOptions()
        options.organization_id = ORGANIZATION_ID
        options.scopes = 'openid profile email offline_access'

        return options

    def code_authentication_options(self):
        return CodeAuthenticationOptions()

    def get_user_info(self, user_id: str):
        return self.users.get_user(user_id)[0]

    
