from danoan.word_def.plugins.modules import english_collins
from danoan.word_def.core import api, exception, model

import io
from pathlib import Path
import pycountry
import pytest
import toml
from types import SimpleNamespace

SCRIPT_FOLDER = Path(__file__).parent


def test_language():
    language_code = english_collins.AdapterFactory().get_language()
    assert pycountry.languages.get(alpha_3=language_code) is not None
    assert language_code == "eng"


def test_adapter_no_config_file_error():
    af = english_collins.AdapterFactory()

    with pytest.raises(exception.ConfigurationFileRequiredError) as e:
        af.get_adapter()
        assert e.type == exception.ConfigurationFileRequiredError


def test_plugin_compatibility():
    assert api.is_plugin_compatible(english_collins.AdapterFactory())


@pytest.mark.parametrize(
    "method_name,response_filepath",
    [
        ("get_definition", SCRIPT_FOLDER / "input" / "legitim.json"),
        ("get_pos_tag", SCRIPT_FOLDER / "input" / "legitim.json"),
    ],
)
def test_adapter(monkeypatch, method_name: str, response_filepath: Path):
    af = english_collins.AdapterFactory()

    def mock_api_call(self, word: str):
        with open(response_filepath, "r") as f:
            mock_response = SimpleNamespace(text=f.read(), status_code=200)
            return mock_response

    monkeypatch.setattr(english_collins.Adapter, f"_{method_name}_api", mock_api_call)

    ss = io.StringIO()
    mock_config = {"entrypoint": "", "secret_key": ""}
    toml.dump(mock_config, ss)
    ss.seek(io.SEEK_SET)

    list_of_results = af.get_adapter(ss).__getattribute__(method_name)("dontcare")
    assert len(list_of_results) > 0


@pytest.mark.parametrize(
    "method_name",
    [
        "get_definition",
        "get_pos_tag",
    ],
)
def test_adapter_error(monkeypatch, method_name: str):
    af = english_collins.AdapterFactory()

    def mock_api_call(self, word: str):
        mock_response = SimpleNamespace(text="", status_code=404)
        return mock_response

    monkeypatch.setattr(english_collins.Adapter, f"_{method_name}_api", mock_api_call)

    ss = io.StringIO()
    mock_config = {"entrypoint": "", "secret_key": ""}
    toml.dump(mock_config, ss)
    ss.seek(io.SEEK_SET)

    with pytest.raises(exception.UnexpectedResponseError) as e:
        af.get_adapter(ss).__getattribute__(method_name)("dontcare")
        assert e.value.status_code == 404
