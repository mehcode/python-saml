from saml import client
from test_schema import build_authentication_request_simple
from urllib.parse import quote_plus


def test_relay_state():
    target = build_authentication_request_simple()
    state = 'http://localhost:8080/'
    uri, _ = client.send('http://localhost', target.serialize(), state)

    relay_state_part = 'RelayState=%s' % quote_plus(state)
    assert relay_state_part in uri
