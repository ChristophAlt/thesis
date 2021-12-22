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
        return "Round(duration={0}, objective={1}, n={2})".format(
            self.__duration, self.__objective, self.__n
        )
