from __future__ import annotations

import logging
import time
from unittest import TestCase

import responses

from pynect.api.authentication import (AuthenticationEnum,
                                       AuthenticationFactory,
                                       BasicAuthentication,
                                       BearerAuthentication)
from pynect.utils import configure_logger, timeit


class TestAuthentication(TestCase):
    logger: logging.Logger = configure_logger('TestAuthentication')

    @timeit(logger)
    def test_authentication_factory_basic(self):
        # build object from factory
        auth = AuthenticationFactory.get(
            AuthenticationEnum.BASIC,
            {'user': 'isearch', 'password': 'basic_auth_pw'}
        )
        self.assertIsInstance(auth, BasicAuthentication)
        # authenticate, setup the session
        auth()
        expected_auth = ('isearch', 'basic_auth_pw')
        current_auth = auth.session.auth
        self.assertTupleEqual(current_auth, expected_auth)

    @responses.activate
    def test_authentication_factory_bearer(self):
        # setup fake response
        auth_url = 'https://auth.pynect.com/oauth/token'
        token = "54692028ran1595eebed1765ec691ca04b"
        responses.add(responses.POST, auth_url, json={
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": 7200,
            "scope": "users.read users.write content.read"

        }, status=200)

        # build object from factory
        auth = AuthenticationFactory.get(AuthenticationEnum.BEARER, {
            'client_id': '9d244454faee7d90fa32b25302fcf6507',
            'client_secret': '4f10c5309926ce099020ee9a76401c508e',
            'token_url': auth_url,
        })
        self.assertIsInstance(auth, BearerAuthentication)
        # authenticate, setup the session
        auth()
        expected_headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        current_headers = auth.session.headers
        self.assertDictEqual(current_headers, expected_headers)

    def test_authentication_factory_invalid_type(self):
        self.assertRaises(
            ValueError,
            AuthenticationFactory.get, 'test', {}
        )
