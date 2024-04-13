from time import sleep
from typing import List, Tuple
import signal
import sys


class Grid:

    def __init__(self, w, h):
        self._w = w
        self._h = h
        self._grid = [[0 for _ in range(self._w)] for _ in range(self._h)]

    def __repr__(self):
        return "\n".join([" ".join(map(lambda x: ' ' if x == 0 else '◼', row)) for row in self._grid])

    def __str__(self):
        return "\n".join([" ".join(map(lambda x: ' ' if x == 0 else '◼', row)) for row in self._grid])

    def _is_cell_valid(self, r, c):
        return r >= 0 and r < self._h and c >= 0 and c < self._w

    def _update_cells(self, cells, value):
        for r, c in cells:
            if self._is_cell_valid(r, c):
                self._grid[r][c] = value

    def clear_cells(self, cells: List[Tuple]):
        self._update_cells(cells, 0)

    def set_cells(self, cells: List[Tuple]):
        self._update_cells(cells, 1)

    def get_cell_value(self, cell):
        r, c = cell
        return self._grid[r][c] if self._is_cell_valid(r, c) else 0


class GridGame:

    def __init__(self, grid=None):
        if grid:
            self._grid = grid
        else:
            self._grid = Grid(30, 30)

    def _sigint_handler(self, signal, frame):
        self._toggle_cursor()
        sys.exit(0)

    def _init_state(self):
        pass

    def _read_controls(self):
        pass

    def _update_state(self):
        pass

    # ANSI escape sequences
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    def _toggle_cursor(self):
        print('\033[?25l', end="")

    # ANSI escape sequences
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    def _cursorup(self, lines):
        print(f"\r\033[{lines}A", end="")

    def tick(self):
        self._toggle_cursor()
        signal.signal(signal.SIGINT, self._sigint_handler)
        self._init_state()
        while (True):
            print(self._grid)
            self._cursorup(30)
            self._read_controls()
            self._update_state()
            sleep(0.3)
