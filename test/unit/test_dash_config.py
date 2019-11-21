import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from lqx_config import LqxConfig


@pytest.fixture
def lqx_conf(**kwargs):
    defaults = {
        'rpcuser': 'lqxrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    lqx_config = lqx_conf()
    creds = LqxConfig.get_rpc_creds(lqx_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'lqxrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 29241

    lqx_config = lqx_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = LqxConfig.get_rpc_creds(lqx_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'lqxrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', lqx_conf(), re.M)
    creds = LqxConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'lqxrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 15784


def test_slurp_config_file():
    import tempfile

    lqx_config = """# basic settings
#testnet=1 # TESTNET
server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    expected_stripped_config = """server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    with tempfile.NamedTemporaryFile(mode='w') as temp:
        temp.write(lqx_config)
        temp.flush()
        conf = LqxConfig.slurp_config_file(temp.name)
        assert conf == expected_stripped_config
