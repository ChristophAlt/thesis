class DriverRound:
    def __init__(self, duration, device, n):
        self.__duration = duration
        self.__device = device
        self.__n = n

    @property
    def duration(self):
        return self.__duration

    @property
    def device(self):
        return self.__device

    @property
    def n(self):
        return self.__n

    def __repr__(self):
        return "Round(duration={0}, device={1}, n={2})".format(
            self.__duration, self.__device, self.__n
        )
