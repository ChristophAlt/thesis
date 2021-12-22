from typing import List

from lib.round import Round


class Experiment:
    def __init__(self, name: str, input_file: str, parameters, rounds: List[Round]):
        self.__name = name
        self.__input_file = input_file
        self.__parameters = parameters
        self.__rounds = rounds

    @property
    def name(self) -> str:
        return self.__name

    @property
    def input_file(self) -> str:
        return self.__input_file

    @property
    def parameters(self):
        return self.__parameters

    @property
    def rounds(self) -> List[Round]:
        return self.__rounds

    def __repr__(self) -> str:
        return "Experiment(name={0}, input_file={1}, parameters={2})".format(
            self.__name, self.__input_file, self.__parameters
        )
