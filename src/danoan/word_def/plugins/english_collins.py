from danoan.dictionaries.collins.core import api as collins_api, model as collins_model

from bs4 import BeautifulSoup
from dataclasses import dataclass
import json
from pathlib import Path
import pycountry
from typing import List, Optional
import toml


@dataclass
class Configuration:
    entrypoint: str
    secret_key: str


class Adapter:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def get_definition(self, word: str) -> List[str]:
        response = collins_api.get_best_matching(
            self.configuration.entrypoint,
            self.configuration.secret_key,
            collins_model.Language.English,
            word,
            collins_model.Format.JSON,
        )

        if response.status_code == 200:
            response_json = json.loads(response.text)
            html_data = response_json["entryContent"]
            html_soup = BeautifulSoup(html_data, "lxml")

            list_of_span_defs = html_soup.css.select(".def")
            list_of_definitions = list(map(lambda x: x.contents[0], list_of_span_defs))
            return list_of_definitions
        else:
            # TODO: Implement exception.
            pass


def get_language() -> str:
    return pycountry.languages.get(name="english").alpha_3


def get_adapater(configuration_filepath: Optional[Path] = None) -> str:
    if configuration_filepath is None:
        # TODO: Implement exception.
        pass

    with open(configuration_filepath, "r") as f:
        configuration = toml.load(f)
        return Adapter(configuration)
