from sudoku_decision import Sudoku
from dataset import dataset

if __name__ == '__main__':
    for data in dataset:
        sudoku = Sudoku(data['task'])
        sudoku.run()
        [print(i) for i in sudoku.task]
        print('*' * 10)
