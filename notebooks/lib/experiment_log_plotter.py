import matplotlib.pyplot as plt
import numpy as np


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
        self.__markers = ["x", "o", "v", "^", ".", "+", "d"]
        self.__use_iterations = False
        self.__every_n = []
        self.__title = ""
        self.__objective_min = 0

    def add_experiment(self, experiment, name=None, every_n=1):
        self.__experiments.append(experiment)
        self.__every_n.append(every_n)
        if name:
            self.__names.append(name)
        else:
            self.__names.append(experiment.name)

    def figsize(self, figsize):
        self.__figsize = figsize

    def ylim(self, ylim):
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

    def plot(self, filename=None):
        timestamps, objectives = ExperimentLogPlotter._prepare_experiments(
            self.__experiments, self.__objective_min, self.__ylim
        )

        plt.figure(figsize=self.__figsize)

        plt.ylim(self.__ylim)
        plt.yticks(self.__yticks)
        plt.xlabel(self.__xlabel)
        plt.ylabel(self.__ylabel)
        plt.grid(self.__grid, which=self.__which_grid)
        plt.xlim((0, ExperimentLogPlotter._max_timestamp(timestamps)))
        plt.title(self.__title)

        for i in range(len(timestamps)):
            timestamp = timestamps[i][:: self.__every_n[i]]
            objective = objectives[i][:: self.__every_n[i]]

            if self.__use_iterations:
                timestamp = np.arange(len(timestamp)) * self.__every_n[i]

            plt.loglog(timestamp, objective, marker=self.__markers[i])

        plt.legend(self.__names, loc="upper right")
        plt.autoscale(axis="x")
        plt.xlim(xmin=0)

        if filename:
            plt.savefig(filename, transparent=True)

    @staticmethod
    def _max_timestamp(timestamps):
        max_timestamp = -np.inf
        for timestamp in timestamps:
            current_max = timestamp.max()
            if current_max > max_timestamp:
                max_timestamp = current_max
        return max_timestamp

    @staticmethod
    def _prepare_experiments(experiments, min_objective, cut_off=1e-4):
        timestamps = []
        objectives = []

        for i, experiment in enumerate(experiments):
            timestamps_arr = np.cumsum(
                [rnd.duration / 1000 for rnd in experiment.rounds]
            )
            objectives_arr = np.array([rnd.objective for rnd in experiment.rounds])

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

        return timestamps, objectives
