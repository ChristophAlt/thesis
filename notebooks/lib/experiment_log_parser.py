from abc import abstractmethod


class ExperimentLogParser:
    @abstractmethod
    def parse(self, file_path):
        pass
