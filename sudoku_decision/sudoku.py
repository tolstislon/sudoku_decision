from itertools import chain
from typing import List, Iterable

MATRIX = List[List[int]]


class Sudoku:

    def __init__(self, task: MATRIX):
        self._task = task
        self._max_iteration = 100

    @property
    def task(self):
        return self._task

    @staticmethod
    def _cleaning(line: Iterable):
        return [list(value)[0] if isinstance(value, set) and len(value) == 1 else value for value in line]

    @staticmethod
    def _only_value(line: Iterable):
        return {i for i in line if not isinstance(i, set) and i != 0}

    def _line(self, line: Iterable):
        """"""
        line = list(line)
        e = []
        for value in line:
            if value == 0:
                default = set(range(1, 10))
                value = default - self._only_value(line)
            elif isinstance(value, set):
                value = value - self._only_value(line)
            e.append(value)
        return self._cleaning(e)

    def _horizontal(self):
        body = [self._line(i) for i in self.task]
        self._task = body

    def _vertical(self):
        body = [self._line(i) for i in zip(*self.task)]
        self._task = [list(i) for i in zip(*body)]

    def _block(self):
        n = 3
        for c in range(0, n * n, n):
            for b in range(0, n * n, n):
                j = [self.task[i + c][b: b + n] for i in range(n)]
                u = self._line(chain(*j))
                u = self._line(u)
                r = [u[i:i + 3] for i in range(0, n * n, n)]
                for i, v in enumerate(r):
                    self._task[i + c][b: b + n] = v

    def _check(self):
        return all(all(isinstance(f, int) for f in i) for i in self.task)

    def run(self):
        for i in range(self._max_iteration):
            self._horizontal()
            self._vertical()
            self._block()
            if self._check():
                break

    def __repr__(self):
        return '\n'.join([' '.join(str(a) for a in i) for i in self.task])
