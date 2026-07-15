"""DNS Authenticator for UKFast's SafeDNS service."""
import logging
from typing import Any
from typing import Optional

from requests import HTTPError

from certbot import errors
from certbot.plugins import dns_common_lexicon

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://my.ukfast.co.uk/applications/index.php'


class Authenticator(dns_common_lexicon.LexiconDNSAuthenticator):
    """DNS Authenticator for UKFast's SafeDNS

    This Authenticator uses the SafeDNS API to fulfill a dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record (if you are using SafeDNS for DNS).'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._add_provider_option('auth_token',
                                  f'API Application Token for SafeDNS account, obtained from {ACCOUNT_URL}',
                                  'auth_token')

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds: int = 30) -> None:  # pylint: disable=arguments-differ
        super().add_parser_arguments(add, default_propagation_seconds)
        add('credentials', help='SafeDNS credentials INI file.')

    def more_info(self) -> str:
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the SafeDNS API.'

    @property
    def _provider_name(self) -> str:
        return 'safedns'

    def _handle_http_error(self, e: HTTPError, domain_name: str) -> errors.PluginError:
        hint = None
        if str(e).startswith('400 Client Error:'):
            hint = 'Are your API key and Secret key values correct?'

        hint_disp = f' ({hint})' if hint else ''

        return errors.PluginError(f'Error determining zone identifier for {domain_name}: '
                                  f'{e}.{hint_disp}')

    def _handle_general_error(self, e: Exception, domain_name: str) -> Optional[errors.PluginError]:
        if domain_name in str(e) and str(e).endswith('not found'):
            return None

        return super()._handle_general_error(e, domain_name)
