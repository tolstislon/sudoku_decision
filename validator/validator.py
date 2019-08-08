from itertools import chain


class Validator:

    def __init__(self, n=3):
        self._data = []
        self._number = n
        self._amount = n ** 2

    def __line(self, line):
        assert len({i for i in line if isinstance(i, int) and i}) == self._amount

    def __horizontal(self):
        [self.__line(i) for i in self._data]

    def __vertical(self):
        [self.__line(i) for i in zip(*self._data)]

    def __block(self):
        for row in range(0, self._amount, self._number):
            for col in range(0, self._amount, self._number):
                line = [self._data[i + row][col: col + self._number] for i in range(self._number)]
                self.__line(chain(*line))

    def run(self, data):
        self._data = data
        try:
            self.__horizontal()
            self.__vertical()
            self.__block()
        except AssertionError:
            return False
        else:
            return True
