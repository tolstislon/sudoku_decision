import re
import tkinter as tk
from typing import Union

from .constant import VERSION, WIDTH, HEIGHT, BUTTON_FONT, ENTRY_BLOCK_FONT
from .enums import Event, Color
from .sudoku_solver import SudokuSolver
from itertools import chain


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
    def _validate(event: str, num: str, symbol: str) -> bool:
        if Event(event) is Event.ENTER and num == '0':
            if re.match(r'^[1-9]$', symbol):
                return True
        elif Event(event) is Event.DELETE:
            return True
        return False

    def _create_grid(self) -> None:
        validate_command = self.register(self._validate)
        for row_block in range(3):
            for col_block in range(3):
                frame_block = FrameBlock(self)
                for row in range(3):
                    for col in range(3):
                        wrapper = WrapFrame(frame_block)
                        block = tk.Entry(
                            wrapper,
                            width=2,
                            bd=1,
                            font=ENTRY_BLOCK_FONT,
                            validate='key',
                            validatecommand=(validate_command, '%d', '%i', '%S'),
                            justify=tk.CENTER,
                            state=tk.NORMAL,
                            insertbackground=Color.BLACK,
                            insertwidth=1
                        )
                        setattr(block, 'element_position', {
                            'row': row_block * 3 + row,
                            'col': col_block * 3 + col
                        })
                        self._blocks.append(block)
                        block.pack()
                        wrapper.grid(row=row, column=col)
                frame_block.grid(row=row_block, column=col_block, pady=2, padx=2)
        self._blocks.sort(key=lambda x: (x.element_position['row'], x.element_position['col']))

    def _start_command(self) -> None:
        if hasattr(self, '_info_label'):
            self._info_label.destroy()
            del self._info_label

        matrix = [[0 for _ in range(9)] for _ in range(9)]
        self._button['state'] = tk.DISABLED
        for block in self._blocks:
            block['state'] = tk.DISABLED
            value = block.get()
            if value:
                matrix[block.element_position['row']][block.element_position['col']] = int(value)
                setattr(block, '_base_value', True)

        try:
            for row in range(9):
                row_data = [i for i in matrix[row] if i != 0]
                assert len(row_data) == len(set(row_data))
                col_data = [matrix[row][i] for i in range(9) if matrix[row][i] != 0]
                assert len(col_data) == len(set(col_data))

            for row in range(0, 9, 3):
                for col in range(0, 9, 3):
                    block_data = [matrix[i + row][col: col + 3] for i in range(3)]
                    block_data = [i for i in chain(*block_data) if i != 0]
                    assert len(block_data) == len(set(block_data))

        except AssertionError:
            self._info_label = tk.Label(self, text='Invalid data', font='arial 12', foreground='red')
            self._info_label.grid(row=4, column=1)
            self._button['state'] = tk.NORMAL
            for block in self._blocks:
                block['state'] = tk.NORMAL
                setattr(block, '_base_value', False)
        else:
            sudoku = SudokuSolver(matrix)
            sudoku.run()
            for r in range(9):
                for c in range(9):
                    self.set_value(sudoku.data[r][c], r, c)

            self._info_label = tk.Label(self, text=f'time: {round(sudoku.duration, 4)} s', font='arial 10')
            self._info_label.grid(row=4, column=1)

    def _reset_command(self) -> None:
        for block in self._blocks:
            block['state'] = tk.NORMAL
            block.delete(0, None)
            setattr(block, '_base_value', False)
        self._button['state'] = tk.NORMAL
        if hasattr(self, '_info_label'):
            self._info_label.destroy()
            del self._info_label

    def _create_button_start(self) -> None:
        self._button = tk.Button(self, text='Start', font=BUTTON_FONT, command=self._start_command)
        self._button.grid(row=4, column=0)

    def _create_button_reset(self) -> None:
        self._button_reset = tk.Button(self, text='Reset', font=BUTTON_FONT, command=self._reset_command)
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
