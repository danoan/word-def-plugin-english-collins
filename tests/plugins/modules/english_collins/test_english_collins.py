from danoan.word_def.plugins.modules import english_collins
from danoan.word_def.core import api, exception, model

from io import StringIO
from pathlib import Path
import pytest
from types import SimpleNamespace

SCRIPT_FOLDER = Path(__file__).parent


def test_language():
    af = english_collins.AdapterFactory()
    assert af.get_language() == "eng"


def test_adapter_no_config_file_error():
    af = english_collins.AdapterFactory()

    with pytest.raises(exception.ConfigurationFileRequiredError) as e:
        af.get_adapter()
        assert e.type == exception.ConfigurationFileRequiredError


def test_plugin_compatibility():
    assert api.is_plugin_compatible(english_collins.AdapterFactory())


def test_adapter_get_definition_handle():
    af = english_collins.AdapterFactory()

    mock_config_filepath = SCRIPT_FOLDER / "input" / "config.toml"
    with open(mock_config_filepath, "r") as f:
        adapter = af.get_adapter(f)

    mock_response_filepath = SCRIPT_FOLDER / "input" / "legitim.json"
    with open(mock_response_filepath, "r") as f:
        mock_response = SimpleNamespace(text=f.read(), status_code=200)
        list_of_definitions = adapter._get_definition_handle(mock_response)

        assert len(list_of_definitions) == 1
        assert list_of_definitions[0].startswith("the part")


def test_adapter_get_definition_handle_with_error():
    af = english_collins.AdapterFactory()

    mock_config_filepath = SCRIPT_FOLDER / "input" / "config.toml"
    with open(mock_config_filepath, "r") as f:
        adapter = af.get_adapter(f)

    mock_response_filepath = SCRIPT_FOLDER / "input" / "legitim.json"
    with open(mock_response_filepath, "r") as f:
        mock_response = SimpleNamespace(text=f.read(), status_code=404)

        with pytest.raises(exception.UnexpectedResponseError) as e:
            list_of_definitions = adapter._get_definition_handle(mock_response)
            assert e.value.status_code == 404


def test_adapter_get_pos_tag_handle():
    af = english_collins.AdapterFactory()

    mock_config_filepath = SCRIPT_FOLDER / "input" / "config.toml"
    with open(mock_config_filepath, "r") as f:
        adapter = af.get_adapter(f)

    mock_response_filepath = SCRIPT_FOLDER / "input" / "legitim.json"
    with open(mock_response_filepath, "r") as f:
        mock_response = SimpleNamespace(text=f.read(), status_code=200)
        list_of_pos_tags = adapter._get_pos_tag_handle(mock_response)

        assert len(list_of_pos_tags) > 0
        assert list_of_pos_tags[0] == model.PosTag.Noun
