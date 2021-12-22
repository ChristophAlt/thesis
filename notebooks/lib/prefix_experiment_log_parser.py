import json

from lib.experiment import Experiment
from lib.experiment_log_parser import ExperimentLogParser
from round import Round


class PrefixExperimentLogParser(ExperimentLogParser):
    def __init__(self, prefix, parameters):
        self.__prefix = prefix
        self.__parameters = parameters

    def parse(self, file_path, no_params=False):
        with open(file_path, "r") as f:
            lines = PrefixExperimentLogParser.filter_lines(f.readlines(), self.__prefix)

            start_idx = 1

            if no_params:
                start_idx = 0

            rounds = []
            for line in lines[start_idx:]:
                round_prop = json.loads(line)
                rounds.append(
                    Round(
                        round_prop["duration"],
                        round_prop["objective"],
                        round_prop["round"],
                    )
                )

            experiment_prop = json.loads(lines[0])

            if no_params:
                name = ""
                input_file = ""
                parameters = {}
            else:
                name = experiment_prop["name"]
                input_file = experiment_prop["inputFile"]
                parameters = {
                    "eta": experiment_prop["eta"],
                    "lambda": experiment_prop["lambda"],
                    "H": experiment_prop["localIterFrac"],
                    "K": experiment_prop["numSplits"],
                }

            return Experiment(name, input_file, parameters, rounds)

    @staticmethod
    def filter_lines(lines, prefix):
        return [
            line[line.find(prefix) + len(prefix):] for line in lines if prefix in line
        ]
