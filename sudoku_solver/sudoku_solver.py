from typing import List, Union, Tuple
import time


class SudokuSolver:

    def __init__(self, data: List[List[int]]):
        self.__data = data
        self.duration = 0.0

    @property
    def data(self):
        return self.__data

    def _validate(self, row: int, col: int, value: int) -> bool:
        """"""
        if all(value != self.__data[row][x] for x in range(9)):
            if all(value != self.__data[x][col] for x in range(9)):
                sector_x, sector_y = 3 * (row // 3), 3 * (col // 3)
                for x in range(sector_x, sector_x + 3):
                    for y in range(sector_y, sector_y + 3):
                        if self.__data[x][y] == value:
                            return False
                return True
        return False

    def _fund_next_cell(self, row: int, col: int) -> Union[Tuple[int, int], Tuple[None, None]]:
        """"""
        for x, y in ((row, col), (0, 0)):
            for r in range(x, 9):
                for c in range(y, 9):
                    if self.__data[r][c] == 0:
                        return r, c
        return None, None

    def _solver(self, row: int = 0, col: int = 0) -> bool:
        """"""
        row, col = self._fund_next_cell(row, col)
        if row is None:
            return True
        for value in range(1, 10):
            if self._validate(row, col, value):
                self.__data[row][col] = value
                if self._solver(row, col):
                    return True
                self.__data[row][col] = 0
        return False

    def run(self) -> None:
        start = time.time()
        self._solver()
        self.duration = time.time() - start
