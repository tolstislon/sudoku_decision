import re
import tkinter as tk
from typing import Union

from .constant import VERSION, WIDTH, HEIGHT
from .enums import Event, Color
from .sudoku_solver import SudokuSolver


class WrapFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bd=0, background=Color.BLACK)


class FrameBlock(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bd=1, background=Color.BLACK)


class Body(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self._blocks = []
        self._create_grid()
        self._create_button_start()
        self._create_button_reset()

    @staticmethod
    def is_okay(event: str, num: str, symbol: str) -> bool:
        if Event(event) is Event.ENTER and num == '0':
            if re.match(r'^[1-9]$', symbol):
                return True
        elif Event(event) is Event.DELETE:
            return True
        return False

    def _create_grid(self):
        okay_command = self.register(self.is_okay)
        for row_block in range(3):
            for col_block in range(3):
                frame_block = FrameBlock(self)
                for row in range(3):
                    for col in range(3):
                        wrapper = WrapFrame(frame_block)
                        block = tk.Entry(wrapper, width=2, bd=1, font='arial 30', validate='key',
                                         validatecommand=(okay_command, '%d', '%i', '%S'), justify=tk.CENTER,
                                         state=tk.NORMAL, insertbackground=Color.BLACK, insertwidth=1)
                        setattr(block, 'element_position', {
                            'row': row_block * 3 + row,
                            'col': col_block * 3 + col
                        })
                        self._blocks.append(block)
                        block.pack()
                        wrapper.grid(row=row, column=col)
                frame_block.grid(row=row_block, column=col_block, pady=2, padx=2)
        self._blocks.sort(key=lambda x: (x.element_position['row'], x.element_position['col']))

    def _start_command(self):
        matrix = [[0 for _ in range(9)] for _ in range(9)]
        self._button['state'] = tk.DISABLED
        for block in self._blocks:
            block['state'] = tk.DISABLED
            value = block.get()
            if value:
                matrix[block.element_position['row']][block.element_position['col']] = int(value)
                setattr(block, '_base_value', True)
        sudoku = SudokuSolver(matrix)
        sudoku.run()
        for r in range(9):
            for c in range(9):
                self.set_value(sudoku.data[r][c], r, c)

    def _reset_command(self):
        for block in self._blocks:
            block['state'] = tk.NORMAL
            block.delete(0, None)
            setattr(block, '_base_value', False)
        self._button['state'] = tk.NORMAL

    def _create_button_start(self):
        self._button = tk.Button(self, text='Start', font='arial 15', command=self._start_command)
        self._button.grid(row=4, column=0)

    def _create_button_reset(self):
        self._button_reset = tk.Button(self, text='Reset', font='arial 15', command=self._reset_command)
        self._button_reset.grid(row=4, column=2)

    def set_value(self, value: Union[str, int], row: int, col: int) -> None:
        elem = list(filter(
            lambda x: x.element_position['row'] == row and x.element_position['col'] == col, self._blocks))[0]
        if not getattr(elem, '_base_value', False):
            elem['state'] = tk.NORMAL
            elem.insert(0, value)
            elem['state'] = tk.DISABLED


class App(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry(f'{WIDTH}x{HEIGHT}')
        self.master.title(f'Sudoku Solver {VERSION}')
        self.master.resizable(False, False)
        self.pack()
        self._body = Body(self)


def app():
    a = App()
    a.mainloop()
