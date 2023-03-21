from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional

from oauthlib.oauth2 import BackendApplicationClient
from requests import Session
from requests_oauthlib import OAuth2Session


class AuthenticationEnum(str, Enum):
    BASIC = 'basic'
    BEARER = 'bearer'
    TOKEN = 'token'


class Authentication:
    def __init__(self):
        self.session: Session = Session()

    def __call__(self):
        raise NotImplementedError

# API Keys
# AWS Signatures
# Kerberos


class BearerAuthentication(Authentication):
    """Class for configuring bearer token auth.

    Args:
        Authentication ([type]): Extends Authentication
    """

    def __init__(self, client_id: str, client_secret: str, token_url: str):
        Authentication.__init__(self)
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__token_url = token_url

    def __call__(self):
        """
        Initialize Session information. Fetch the user token and configures
        it in the session headers.
        """
        client = BackendApplicationClient(client_id=self.__client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=self.__token_url,
            include_client_id=self.__client_id,
            client_secret=self.__client_secret
        )
        access_token = token['access_token']
        self.session.headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }


class TokenAuthentication(Authentication):
    def __init__(self, access_token: str):
        Authentication.__init__(self)
        self.access_token = access_token

    def __call__(self):
        self.session.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }


class BasicAuthentication(Authentication):
    """Class for configuring basic auth.

    Args:
        Authentication ([type]): Extends Authentication
    """

    def __init__(self, user: str, password: str):
        Authentication.__init__(self)
        self.__user = user
        self.__password = password

    def __call__(self):
        """ Initialize Session information """
        self.session.auth = (self.__user, self.__password)
        self.session.verify = False


class AuthenticationFactory(ABC):
    """ Factory that provides an authentication object. """

    @staticmethod
    def get(auth_type: str, credentials: dict) -> Authentication:
        """
        Factory method that provides a BasicAuthentication or
        BearerAuthentication class object

        Args:
            auth_type (str): required authentication type: "basic" or "bearer"
            credentials (dict): data dictionary containing the init params.
            For BasicAuthentication user and password.
            For BearerAuthentication client_id, client_secret, token_url.

        Raises:
            ValueError: If an invalid authentication type is provided

        Returns:
            Optional[Authentication]: Authentication object or None
        """
        try:
            auth_options: Dict[str, type[Authentication]] = {
                'basic': BasicAuthentication,
                'bearer': BearerAuthentication,
                'token': TokenAuthentication,
            }
            return auth_options[auth_type](**credentials)
        except KeyError:
            raise ValueError(f'Authentication ({auth_type}) type invalid')
