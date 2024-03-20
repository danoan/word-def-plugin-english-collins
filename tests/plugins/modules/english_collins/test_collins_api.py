from danoan.word_def.plugins.modules import english_collins
from danoan.word_def.core import api, exception, model

import io
from pathlib import Path
import pytest
import toml
import warnings

SCRIPT_FOLDER = Path(__file__).parent


@pytest.fixture(scope="session")
def entrypoint(pytestconfig):
    v = pytestconfig.getoption("entrypoint")
    if v is None:
        warnings.warn("The API entrypoint is not specified. Tests won't be executed.")
    return pytestconfig.getoption("entrypoint", skip=True)


@pytest.fixture(scope="session")
def secret_key(pytestconfig):
    v = pytestconfig.getoption("secret_key")
    if v is None:
        warnings.warn("The API secret key is not specified. Tests won't be executed.")
    return pytestconfig.getoption("secret_key", skip=True)


@pytest.mark.api
@pytest.mark.parametrize(
    "method_name,word", [("get_definition", "legitim"), ("get_pos_tag", "legitim")]
)
def test_adapter(entrypoint: str, secret_key: str, method_name: str, word: str):
    af = english_collins.AdapterFactory()

    ss = io.StringIO()
    mock_config = {"entrypoint": entrypoint, "secret_key": secret_key}
    toml.dump(mock_config, ss)
    ss.seek(io.SEEK_SET)

    list_of_results = af.get_adapter(ss).__getattribute__(method_name)(word)
    assert len(list_of_results) > 0
