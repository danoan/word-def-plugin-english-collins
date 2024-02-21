from danoan.word_def.core import model, exception

from danoan.dictionaries.collins.core import api as collins_api, model as collins_model

from bs4 import BeautifulSoup
from dataclasses import dataclass
import importlib
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
            # TODO: This could be improved. The response contains much more
            # tagged information than the definition but it is not that
            # straightforward to parse, that is why we are limiting ourselves
            # to take the definition.
            # Due to how the HTML is written, the text of the definition is
            # sometimes spread over more than two tags. We are limiting ourselves
            # to the `def` tag. We use the character count limit of 16 to avoid
            # situations in which we collect incomplete phrasings.
            for potential_definition in list_of_span_defs:
                content = potential_definition.contents[0].strip()
                if len(content) > 16:
                    list_of_definitions.append(content)
            return list_of_definitions
        else:
            raise exception.UnexpectedResponseError(response.status_code, response.text)

    def get_definition(self, word: str) -> List[str]:
        response = self._get_definition_api(word)
        return self._get_definition_handle(response)

    @staticmethod
    def _to_pos_tag(pos_tag_string: str):
        string_to_pos_tag = {
            "adjective": model.PosTag.Adjective,
            "adverb": model.PosTag.Adverb,
            "auxiliary": model.PosTag.Auxiliary,
            "conjunction": model.PosTag.Conjunction,
            "determiner": model.PosTag.Determiner,
            "interjection": model.PosTag.Interjection,
            "exclamation": model.PosTag.Interjection,
            "noun": model.PosTag.Noun,
            "numeral": model.PosTag.Numeral,
            "particle": model.PosTag.Particle,
            "pronoun": model.PosTag.Pronoun,
            "verb": model.PosTag.Verb,
        }

        if pos_tag_string in string_to_pos_tag:
            return string_to_pos_tag[pos_tag_string]
        else:
            return ""

    def _get_pos_tag_api(self, word: str):
        return collins_api.get_best_matching(
            self.configuration.entrypoint,
            self.configuration.secret_key,
            collins_model.Language.English,
            word,
            collins_model.Format.JSON,
        )

    def _get_pos_tag_handle(self, response: collins_api.requests.Response):
        if response.status_code == 200:
            response_json = json.loads(response.text)
            html_data = response_json["entryContent"]
            html_soup = BeautifulSoup(html_data, "lxml")

            list_of_span_pos = html_soup.css.select(".pos")
            return list(
                set(map(lambda x: self._to_pos_tag(x.contents[0]), list_of_span_pos))
            )
        else:
            raise exception.UnexpectedResponseError(response.status_code, response.text)

    def get_pos_tag(self, word: str) -> List[model.PosTag]:
        response = self._get_pos_tag_api(word)
        return self._get_pos_tag_handle(response)


class AdapterFactory:
    def version(self):
        return importlib.metadata.version("word-def-plugin-english-collins")

    def get_language(self) -> str:
        return pycountry.languages.get(name="english").alpha_3

    def get_adapter(self, configuration_stream: Optional[TextIO] = None) -> Adapter:
        if configuration_stream is None:
            raise exception.ConfigurationFileRequiredError()

        configuration = Configuration(**toml.load(configuration_stream))
        return Adapter(configuration)
