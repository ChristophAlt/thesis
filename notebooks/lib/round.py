class Round:
    def __init__(self, duration, objective, n):
        self.__duration = duration
        self.__objective = objective
        self.__n = n

    @property
    def duration(self):
        return self.__duration

    @property
    def objective(self):
        return self.__objective

    @property
    def n(self):
        return self.__n

    def __repr__(self):
        return "Round(duration={0}, objective={1}, n={2})".format(
            self.__duration, self.__objective, self.__n
        )
