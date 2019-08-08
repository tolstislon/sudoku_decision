import pytest
from sudoku_solver import SudokuSolver
from validator import Validator
from dataset import dataset


@pytest.mark.parametrize('task', dataset)
def test_solver(task):
    sudoku = SudokuSolver(task['task'])
    sudoku.run()
    assert Validator().run(sudoku.data)
