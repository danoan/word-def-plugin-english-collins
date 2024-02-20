from danoan.word_def.core import exception

from danoan.dictionaries.collins.core import api as collins_api, model as collins_model

from bs4 import BeautifulSoup
from dataclasses import dataclass
import json
import pycountry
from typing import List, Optional, TextIO
import toml


@dataclass
class Configuration:
    entrypoint: str
    secret_key: str


class Adapter:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def _get_definition_api(self, word: str):
        return collins_api.get_best_matching(
            self.configuration.entrypoint,
            self.configuration.secret_key,
            collins_model.Language.English,
            word,
            collins_model.Format.JSON,
        )

    def _get_definition_handle(self, response: collins_api.requests.Response):
        if response.status_code == 200:
            response_json = json.loads(response.text)
            html_data = response_json["entryContent"]
            html_soup = BeautifulSoup(html_data, "lxml")

            list_of_span_defs = html_soup.css.select(".def")
            list_of_definitions = []
            for potential_definition in list_of_span_defs:
                content = potential_definition.contents[0].strip()
                if len(content) > 3:
                    list_of_definitions.append(content)
            return list_of_definitions
        else:
            raise exception.UnexpectedResponseError(
                response.status_code, response.text)

    def get_definition(self, word: str) -> List[str]:
        response = self._get_definition_api(word)
        return self._get_definition_handle(response)


class AdapterFactory:
    def get_language(self) -> str:
        return pycountry.languages.get(name="english").alpha_3

    def get_adapter(self, configuration_stream: Optional[TextIO] = None) -> Adapter:
        if configuration_stream is None:
            raise exception.ConfigurationFileRequiredError()

        configuration = Configuration(**toml.load(configuration_stream))
        return Adapter(configuration)
