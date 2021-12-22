class DriverRound:
    def __init__(self, duration: float, device: str, n: int):
        self.__duration = duration
        self.__device = device
        self.__n = n

    @property
    def duration(self) -> float:
        return self.__duration

    @property
    def device(self) -> str:
        return self.__device

    @property
    def n(self) -> int:
        return self.__n

    def __repr__(self) -> str:
        return "Round(duration={0}, device={1}, n={2})".format(
            self.__duration, self.__device, self.__n
        )
