"""Tests for certbot_dns_safedns.dns_safedns."""
import sys
from unittest import mock

import pytest
from requests import Response
from requests.exceptions import HTTPError

from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.tests import util as test_util

AUTH_TOKEN = 'foo'


class AuthenticatorTest(test_util.TempDirTestCase,
                        dns_test_common_lexicon.BaseLexiconDNSAuthenticatorTest):

    DOMAIN_NOT_FOUND = Exception('No domain found')
    LOGIN_ERROR = HTTPError('400 Client Error: ...', response=Response())

    def setUp(self):
        super().setUp()

        from certbot_dns_safedns.dns_safedns import Authenticator

        path = os.path.join(self.tempdir, 'file.ini')
        credentials = {
            "safedns_auth_token": AUTH_TOKEN,
        }
        dns_test_common.write(credentials, path)

        self.config = mock.MagicMock(safedns_credentials=path,
                                     safedns_propagation_seconds=0)  # don't wait during tests

        self.auth = Authenticator(self.config, 'safedns')


if __name__ == "__main__":
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))  # pragma: no cover
