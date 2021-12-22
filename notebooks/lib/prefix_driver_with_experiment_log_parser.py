import json
from itertools import groupby

from lib.driver_round import DriverRound
from lib.experiment import Experiment
from lib.experiment_log_parser import ExperimentLogParser
from lib.prefix_experiment_log_parser import PrefixExperimentLogParser
from lib.round import Round


class PrefixDriverWithExperimentLogParser(ExperimentLogParser):
    def __init__(self, prefix, parameters):
        self.__prefix = prefix
        self.__parameters = parameters

    def parse(self, driver_log_path, file_path, no_params=False):
        with open(driver_log_path, "r") as f_d:
            lines_d = PrefixExperimentLogParser.filter_lines(
                f_d.readlines(), self.__prefix
            )

            with open(file_path, "r") as f_f:
                lines_f = PrefixExperimentLogParser.filter_lines(
                    f_f.readlines(), self.__prefix
                )

                rounds_d = []
                for line in lines_d[1:]:
                    round_prop = json.loads(line)
                    rounds_d.append(
                        DriverRound(
                            round_prop["duration"],
                            round_prop["device"],
                            round_prop["round"],
                        )
                    )

                rnd_duration = {}
                for rnd, devices in groupby(rounds_d, lambda r: r.n):
                    rnd_duration[rnd] = max(devices, key=lambda d: d.duration).duration

                experiment_prop = json.loads(lines_d[0])

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

                # device = json.loads(lines_f[0])['device']

                # rnd_duration = {rnd.n: rnd.duration for rnd in rounds_d if rnd.device == device}

                rounds_f = []
                for line in lines_f[0:]:
                    round_prop = json.loads(line)
                    rounds_f.append(
                        Round(
                            rnd_duration[round_prop["duration"]],
                            round_prop["objective"],
                            round_prop["round"],
                        )
                    )

            return Experiment(name, input_file, parameters, rounds_f)

    @staticmethod
    def filter_lines(lines, prefix):
        return [
            line[line.find(prefix) + len(prefix):] for line in lines if prefix in line
        ]
