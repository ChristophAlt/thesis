from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


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
        self.__markers = [
            "x",
            "o",
            "v",
            "^",
            "h",
            "+",
            "d",
            "p",
            "*",
            "s",
            "<",
            ">",
            "H",
        ]
        self.__use_iterations = False
        self.__every_n = []
        self.__title = []
        self.__subplots = []
        self.__objective_mins = {}

    def add_experiment(self, experiment, subplot=1, name=None, every_n=1):
        self.__experiments.append(experiment)
        self.__every_n.append(every_n)
        self.__subplots.append(subplot)
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

    def title(self, title, subplot=1):
        self.__title.append(title)

    def add_min_objectives(self, objective, subplot):
        self.__objective_mins[subplot] = objective

    def plot(self, filename=None):
        timestamps, objectives = ExperimentDoubleLogPlotter._prepare_experiments(
            self.__experiments, self.__objective_mins, self.__subplots, self.__ylim
        )

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
            # axarr[i].set_xlim((0, ExperimentLogPlotter._max_timestamp(timestamps)))
            axarr[i].set_title(self.__title[i])

        for i in range(len(timestamps)):
            timestamp = timestamps[i][:: self.__every_n[i]]
            objective = objectives[i][:: self.__every_n[i]]
            subplot = self.__subplots[i]
            name = self.__names[i]
            legends[subplot - 1].append(name)

            if self.__use_iterations:
                timestamp = np.arange(len(timestamp)) * self.__every_n[i]

            axarr[subplot - 1].loglog(timestamp, objective, marker=self.__markers[i])

        for i in range(n_subplots):
            axarr[i].legend(legends[i], loc="upper right")
            axarr[i].autoscale(axis="x")
            axarr[i].set_xlim(xmin=0)

        if filename:
            f.savefig(filename, transparent=True)

    @staticmethod
    def _max_timestamp(timestamps):
        max_timestamp = -np.inf
        for timestamp in timestamps:
            current_max = timestamp.max()
            if current_max > max_timestamp:
                max_timestamp = current_max
        return max_timestamp

    @staticmethod
    def _prepare_experiments(experiments, min_objectives, subplots, cut_off=1e-4):
        timestamps = []
        objectives = []

        for i, experiment in enumerate(experiments):
            timestamps_arr = np.cumsum(
                [rnd.duration / 1000 for rnd in experiment.rounds]
            )
            objectives_arr = np.array([rnd.objective for rnd in experiment.rounds])

            # objectives_arr = objectives_arr - objectives_arr.min()
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

        # objectives = [objective - min_objective for objective in objectives]

        return timestamps, objectives
