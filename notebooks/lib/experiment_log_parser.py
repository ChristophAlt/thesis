from abc import abstractmethod

from lib.experiment import Experiment


class ExperimentLogParser:
    @abstractmethod
    def parse(self, file_path: str) -> Experiment:
        pass
