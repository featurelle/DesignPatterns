from __future__ import annotations
from abc import ABC, abstractmethod
import json
import os


class DictAnalytics:

    def __init__(self, seq: dict[str, dict], max_info_size: int, analyzer: AnalyzerInterface):
        self.__seq = seq
        self.__max_info_size = max_info_size
        self.__analyzer = analyzer

    def overloaded_dicts(self):
        overloaded = []
        for key, value in self.__seq.items():
            if overload := self.__analyzer.overload(value, self.__max_info_size):
                overloaded.append((key, overload))
        return overloaded


class AnalyzerInterface(ABC):

    @abstractmethod
    def overload(self, dict_: dict, max_len: int):
        pass


class JSONAnalyzer101:

    def json_len(self, json_file):
        result = len(json.dumps(json.load(json_file)))
        json_file.close()
        return result

    def json_str(self, json_file):
        result = json.dumps(json.load(json_file))
        json_file.close()
        return result


class JSONAnalyzer102:

    def json_length(self, json_dict):
        return len(json.dumps(json_dict))

    def json_str(self, json_dict):
        return json.dumps(json_dict)


class JSONFileWrapper:

    def __init__(self, file_path):
        self.__file_path = file_path

    def open(self):
        self.__file = open(self.__file_path)
        return self.__file

    def write(self):
        self.__file = open(self.__file_path, 'w')
        return self.__file

    def close(self):
        self.__file.close()


class AnalyzerJSONAdapter101(AnalyzerInterface, JSONAnalyzer101):

    def overload(self, dict_: dict, max_len: int):
        temp_file_path = 'json.json'
        json_wrapper = JSONFileWrapper(temp_file_path)
        json.dump(dict_, json_wrapper.write())
        json_wrapper.close()
        if self.json_len(json_wrapper.open()) > max_len:
            result = self.json_str(json_wrapper.open())[max_len:]
            os.remove(os.path.join(os.path.dirname(__file__), temp_file_path))  # Не работает никак
            return result
        else:
            return None


class AnalyzerJSONAdapter102(AnalyzerInterface, JSONAnalyzer102):

    def overload(self, dict_: dict, max_len: int):
        if self.json_length(dict_) > max_len:
            return self.json_str(dict_)[max_len:]
        else:
            return None


def some_app():
    dictionaries = {'a': {'beer': 'sober', 'portrait': 'quality'},
                    'b': {'sea': 'fisher'},
                    'c': {'hello': 'how are you?'}}

    adapter1 = AnalyzerJSONAdapter101()
    adapter2 = AnalyzerJSONAdapter102()

    analytics1 = DictAnalytics(dictionaries, 12, adapter1)
    analytics2 = DictAnalytics(dictionaries, 12, adapter2)

    analytics3 = DictAnalytics(dictionaries, 30, adapter1)
    analytics4 = DictAnalytics(dictionaries, 30, adapter2)

    analytics = analytics1, analytics2, analytics3, analytics4

    for analysis in analytics:
        print(analysis.overloaded_dicts())


if __name__ == "__main__":
    some_app()
