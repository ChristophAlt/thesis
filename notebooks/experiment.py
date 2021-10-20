from abc import ABC, abstractmethod
from typing import *

class Experiment:
    def __init__(self, name: str, input_file: str, parameters: List[str], rounds: List[Round]):
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
    def parameters(self) -> List[str]:
        return self.__parameters
    
    @property
    def rounds(self) -> List[Round]:
        return self.__rounds
    
    def __repr__(self) -> str:
        return 'Experiment(name={0}, input_file={1}, parameters={2})'.format(
            self.__name, self.__input_file, self.__parameters)
    
class Round:
    def __init__(self, duration: float, objective: float, n: int):
        self.__duration = duration
        self.__objective = objective
        self.__n = n
        
    @property
    def duration(self) -> float:
        return self.__duration
    
    @property
    def objective(self) -> float:
        return self.__objective
    
    @property
    def n(self) -> int:
        return self.__n
    
    def __repr__(self) -> str:
        return 'Round(duration={0}, objective={1}, n={2})'.format(
            self.__duration, self.__objective, self.__n)
    
class DriverRound:
    def __init__(self, duration: float, device: float, n: int):
        self.__duration = duration
        self.__device = device
        self.__n = n
        
    @property
    def duration(self) -> float:
        return self.__duration
    
    @property
    def device(self) -> float:
        return self.__device
    
    @property
    def n(self) -> n:
        return self.__n
    
    def __repr__(self) -> str:
        return 'Round(duration={0}, device={1}, n={2})'.format(
            self.__duration, self.__device, self.__n)

class ExperimentLogParser:
    @abstractmethod
    def parse(self, file_path: str) -> Experiment:
        pass

class PrefixExperimentLogParser(ExperimentLogParser):
    def __init__(self, prefix: str, parameters: List[str]):
        self.__prefix = prefix
        self.__parameters = parameters
    
    def parse(self, file_path: str, no_params: bool =False) -> Experiment:
        with open(file_path, 'r') as f:
            lines = PrefixExperimentLogParser.filter_lines(f.readlines(), self.__prefix)
            
            start_idx = 1
            
            if no_params:
                start_idx = 0
            
            rounds = []
            for line in lines[start_idx:]:
                round_prop = json.loads(line)
                rounds.append(Round(round_prop['duration'], round_prop['objective'], round_prop['round']))
                
            experiment_prop = json.loads(lines[0])
            
            if no_params:
                name = ''
                input_file = ''
                parameters = {}
            else:
                name = experiment_prop['name']
                input_file = experiment_prop['inputFile']
                parameters = {
                    'eta': experiment_prop['eta'],
                    'lambda': experiment_prop['lambda'],
                    'H': experiment_prop['localIterFrac'],
                    'K': experiment_prop['numSplits']
                }
            
            return Experiment(name, input_file, parameters, rounds)
        
    @staticmethod
    def filter_lines(lines: List[str], prefix: str) -> List[str]:
        return [line[line.find(prefix) + len(prefix):] for line in lines if prefix in line]
    
class PrefixDriverWithExperimentLogParser(ExperimentLogParser):
    def __init__(self, prefix: str, parameters: List[str]):
        self.__prefix = prefix
        self.__parameters = parameters
    
    def parse(self: PrefixDriverWithExperimentLogParser, driver_log_path: str, file_path: str, no_params=False) -> Experiment:
        with open(driver_log_path, 'r') as f_d:
            lines_d = PrefixExperimentLogParser.filter_lines(f_d.readlines(), self.__prefix)
            
            with open(file_path, 'r') as f_f:
                lines_f = PrefixExperimentLogParser.filter_lines(f_f.readlines(), self.__prefix)
                
                rounds_d = []
                for line in lines_d[1:]:
                    round_prop = json.loads(line)
                    rounds_d.append(DriverRound(round_prop['duration'], round_prop['device'], round_prop['round']))

                rnd_duration = {}
                for rnd, devices in groupby(rounds_d, lambda r: r.n):
                    rnd_duration[rnd] = max(devices, key=lambda d: d.duration).duration
                    
                experiment_prop = json.loads(lines_d[0])

                if no_params:
                    name = ''
                    input_file = ''
                    parameters = {}
                else:
                    name = experiment_prop['name']
                    input_file = experiment_prop['inputFile']
                    parameters = {
                        'eta': experiment_prop['eta'],
                        'lambda': experiment_prop['lambda'],
                        'H': experiment_prop['localIterFrac'],
                        'K': experiment_prop['numSplits']
                    }

                #device = json.loads(lines_f[0])['device']
                
                #rnd_duration = {rnd.n: rnd.duration for rnd in rounds_d if rnd.device == device}
                    
                rounds_f = []
                for line in lines_f[0:]:
                    round_prop = json.loads(line)
                    rounds_f.append(Round(rnd_duration[round_prop['duration']], round_prop['objective'], round_prop['round']))
            
            return Experiment(name, input_file, parameters, rounds_f)
        
    @staticmethod
    def filter_lines(lines: List[str], prefix: str) -> List[str]:
        return [line[line.find(prefix) + len(prefix):] for line in lines if prefix in line]

class ExperimentLogPlotter:
    def __init__(self):
        self.__experiments = []
        self.__names = []
        self.__figsize = (8, 6)
        self.__ylim = 1e-4
        self.__yticks = [10e-1, 10e-2, 10e-3, 10e-4]
        self.__xlabel = "Seconds"
        self.__ylabel = ""
        self.__grid = False
        self.__which_grid = "both"
        self.__markers = ['x', 'o', 'v', '^', '.', '+', 'd']
        self.__use_iterations = False
        self.__every_n = []
        self.__title = ""
        self.__objective_min = 0
        
    def add_experiment(self, experiment: Experiment, name: str =None, every_n: int =1) -> None:
        self.__experiments.append(experiment)
        self.__every_n.append(every_n)
        if name:
            self.__names.append(name)
        else:
            self.__names.append(experiment.name)
    
    def figsize(self, figsize: float) -> float:
        self.__figsize = figsize
        
    def ylim(self, ylim: float) -> float:
        self.__ylim = ylim
        
    def yticks(self, ticks):
        self.__yticks = ticks
        
    def ylabel(self, label):
        self.__ylabel = label
        
    def enable_grid(self, which):
        self.__which_grid = which
        
    def use_iterations(self):
        self.__use_iterations = True
        self.__xlabel = "Iterations"
        
    def add_min_objective(self, objective):
        self.__objective_min = objective
    
    def title(self, title):
        self.__title = title
    
    def plot(self, filename: str=None) -> None:
        timestamps, objectives = ExperimentLogPlotter._prepare_experiments(self.__experiments, self.__objective_min, self.__ylim)
        
        plt.figure(figsize=self.__figsize)
        
        plt.ylim(self.__ylim)
        plt.yticks(self.__yticks)
        plt.xlabel(self.__xlabel)
        plt.ylabel(self.__ylabel)
        plt.grid(self.__grid, which=self.__which_grid)
        plt.xlim((0, ExperimentLogPlotter._max_timestamp(timestamps)))
        plt.title(self.__title)
        
        for i in range(len(timestamps)):
            timestamp = timestamps[i][::self.__every_n[i]]
            objective = objectives[i][::self.__every_n[i]]
            
            if self.__use_iterations:
                timestamp = np.arange(len(timestamp)) * self.__every_n[i]

            plt.loglog(timestamp, objective, marker=self.__markers[i])
        
        plt.legend(self.__names, loc='upper right')
        plt.autoscale(axis='x')
        plt.xlim(xmin=0)
        
        if filename:
            plt.savefig(filename, transparent=True)
        
    @staticmethod
    def _max_timestamp(timestamps: List[float]) -> float:
        max_timestamp = -np.inf
        for timestamp in timestamps:
            current_max = timestamp.max()
            if current_max > max_timestamp:
                max_timestamp = current_max
        return max_timestamp
      
    @staticmethod
    def _prepare_experiments(experiments: List[Experiment], min_objective: float, cut_off: float =1e-4) -> Tuple[List[float], List[float]]:
        timestamps = []
        objectives = []
        
        for i, experiment in enumerate(experiments):
            timestamps_arr = np.cumsum([rnd.duration / 1000 for rnd in experiment.rounds])
            objectives_arr = np.array([rnd.objective for rnd in experiment.rounds])
            
            #objectives_arr = objectives_arr - objectives_arr.min()
            objectives_arr = objectives_arr - min_objective
            
            max_idx = -1
            for i, objective in enumerate(objectives_arr):
                if objective < cut_off:
                    max_idx = i
                    break
            
            timestamps.append(timestamps_arr[:max_idx])
            objectives.append(objectives_arr[:max_idx])
        
        min_objective = np.inf
        for objective in objectives:
            current_min = objective.min()
            if current_min < min_objective:
                min_objective = current_min
        
        #objectives = [objective - min_objective for objective in objectives]
        
        return timestamps, objectives

class ExperimentDoubleLogPlotter:
    def __init__(self):
        self.__experiments = []
        self.__names = []
        self.__figsize = (8, 6)
        self.__ylim = 1e-4
        self.__yticks = [10e-1, 10e-2, 10e-3, 10e-4]
        self.__xlabel = "Seconds"
        self.__ylabel = ""
        self.__grid = False
        self.__which_grid = "both"
        self.__markers = ['x', 'o', 'v', '^', 'h', '+', 'd', 'p', '*', 's', '<', '>', 'H']
        self.__use_iterations = False
        self.__every_n = []
        self.__title = []
        self.__subplots = []
        self.__objective_mins = {}
        
    def add_experiment(self, experiment: Experiment, subplot: int =1, name: str =None, every_n: int =1) -> None:
        self.__experiments.append(experiment)
        self.__every_n.append(every_n)
        self.__subplots.append(subplot)
        if name:
            self.__names.append(name)
        else:
            self.__names.append(experiment.name)
    
    def figsize(self, figsize: float) -> float:
        self.__figsize = figsize
        
    def ylim(self, ylim: float) -> float:
        self.__ylim = ylim
        
    def yticks(self, ticks: int) -> int:
        self.__yticks = ticks
        
    def ylabel(self, label: str) -> str:
        self.__ylabel = label
        
    def enable_grid(self, which):
        self.__which_grid = which
        
    def use_iterations(self):
        self.__use_iterations = True
        self.__xlabel = "Iterations"
    
    def title(self, title: str, subplot: int =1) -> None:
        self.__title.append(title)
    
    def add_min_objectives(self, objective: float, subplot: int) -> None:
        self.__objective_mins[subplot] = objective
    
    def plot(self, filename: str =None) -> None:
        timestamps, objectives = ExperimentDoubleLogPlotter._prepare_experiments(self.__experiments, self.__objective_mins, self.__subplots, self.__ylim)
        
        n_subplots = max(self.__subplots)
        
        f, axarr = plt.subplots(nrows=1, ncols=n_subplots, figsize=self.__figsize)
        legends = defaultdict(list)
        
        for i in range(n_subplots):
            axarr[i].set_ylim(self.__ylim)
            axarr[i].set_yticks(self.__yticks)
            axarr[i].set_xticks([10e0, 10e1, 10e2, 10e3, 10e4])
            axarr[i].set_xlabel(self.__xlabel)
            axarr[i].set_ylabel(self.__ylabel)
            axarr[i].grid(self.__grid, which=self.__which_grid)
            #axarr[i].set_xlim((0, ExperimentLogPlotter._max_timestamp(timestamps)))
            axarr[i].set_title(self.__title[i])
        
        for i in range(len(timestamps)):
            timestamp = timestamps[i][::self.__every_n[i]]
            objective = objectives[i][::self.__every_n[i]]
            subplot = self.__subplots[i]
            name = self.__names[i]
            legends[subplot-1].append(name)
            
            if self.__use_iterations:
                timestamp = np.arange(len(timestamp)) * self.__every_n[i]

            axarr[subplot-1].loglog(timestamp, objective, marker=self.__markers[i])
        
        for i in range(n_subplots):
            axarr[i].legend(legends[i], loc='upper right')
            axarr[i].autoscale(axis='x')
            axarr[i].set_xlim(xmin=0)
            
        if filename:
            f.savefig(filename, transparent=True)
        
    @staticmethod
    def _max_timestamp(timestamps: List[float]) -> float:
        max_timestamp = -np.inf
        for timestamp in timestamps:
            current_max = timestamp.max()
            if current_max > max_timestamp:
                max_timestamp = current_max
        return max_timestamp
      
    @staticmethod
    def _prepare_experiments(experiments: List[Experiment], min_objectives: List[float], subplots:List[int], cut_off:float =1e-4) -> Tuple[List[float], List[float]]:
        timestamps = []
        objectives = []
        
        for i, experiment in enumerate(experiments):
            timestamps_arr = np.cumsum([rnd.duration / 1000 for rnd in experiment.rounds])
            objectives_arr = np.array([rnd.objective for rnd in experiment.rounds])
            
            #objectives_arr = objectives_arr - objectives_arr.min()
            objectives_arr = objectives_arr - min_objectives[subplots[i]]
            
            max_idx = -1
            for i, objective in enumerate(objectives_arr):
                if objective < cut_off:
                    max_idx = i
                    break
            
            timestamps.append(timestamps_arr[:max_idx])
            objectives.append(objectives_arr[:max_idx])
        
        min_objective = np.inf
        for objective in objectives:
            current_min = objective.min()
            if current_min < min_objective:
                min_objective = current_min
        
        #objectives = [objective - min_objective for objective in objectives]
        
        return timestamps, objectives