from time import sleep
from typing import List, Tuple

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
        return r >= 0 and r < self._h and c >=0 and c < self._w

    def _update_cells(self, cells, value):
        for r,c in cells:
            if self._is_cell_valid(r, c):
                self._grid[r][c] = value

    def clear_cells(self, cells: List[Tuple]):
        self._update_cells(cells, 0)

    def set_cells(self, cells: List[Tuple]):
        self._update_cells(cells, 1)

    def get_cell_value(self, cell):
        r, c = cell
        return self._grid[r][c] if self._is_cell_valid(r, c) else 0

class Game:

    def __init__(self, grid=None):
        if grid:
            self._grid = grid
        else:
            self._grid = Grid(30, 30)

    def _init_state(self):
        pass

    def _update_state(self):
        pass

    # ANSI escape sequences
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    def _hide_cursor(self):
        print('\033[?25l', end="")

    # ANSI escape sequences
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    def _cursorup(self, lines):
        print(f"\r\033[{lines}A", end="")

    def tick(self):
        self._init_state()
        self._hide_cursor()
        while(True):
            sleep(0.3)
            print(self._grid)
            self._cursorup(30)
            self._update_state()
            # alive, dead = next_state(grid)
            # grid.clear_cells(dead)
            # grid.set_cells(alive)

class GameOfLife(Game):

    def _get_live_neighbors(self, r, c):
        cells = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
        values = [self._grid.get_cell_value(cell) for cell in cells]
        return sum(values)

    def _is_alive(self, r, c):
        return self._grid.get_cell_value((r, c)) == 1

    def _next_state(self):
        ng_alive = []
        ng_dead = []
        for i in range(self._grid._h):
            for j in range(self._grid._w):
                n = self._get_live_neighbors(i, j)
                if self._is_alive(i, j) and n < 2:
                    ng_dead.append((i, j))
                if self._is_alive(i, j) and n >= 2 and n <= 3:
                    ng_alive.append((i, j))
                if self._is_alive(i, j) and n > 3:
                    ng_dead.append((i, j))
                if not self._is_alive(i, j) and n == 3:
                    ng_alive.append((i, j))
        return ng_alive, ng_dead

    def lw_spaceship(self, bl_r, bl_c):
        cells = [(bl_r - 3, bl_c + 1), (bl_r - 3, bl_c + 4), (bl_r - 2, bl_c), (bl_r - 1, bl_c), (bl_r, bl_c), (bl_r, bl_c + 1), (bl_r, bl_c + 2), (bl_r, bl_c + 3), (bl_r - 1, bl_c + 4)]
        self._grid.set_cells(cells)

    def blinker(self, bl_r, bl_c):
        cells = [(bl_r, bl_c), (bl_r, bl_c + 1), (bl_r, bl_c + 2)]
        self._grid.set_cells(cells)

    def _init_state(self):
        self.blinker(4, 4)
        self.blinker(8, 4)
        self.blinker(12, 4)
        self.blinker(16, 4)
        self.blinker(20, 4)
        self.blinker(24, 4)
        self.lw_spaceship(5, 5)
        self.lw_spaceship(10, 10)
        self.lw_spaceship(15, 15)
        self.lw_spaceship(25, 25)

    def _update_state(self):
        alive, dead = self._next_state()
        self._grid.clear_cells(dead)
        self._grid.set_cells(alive)



GameOfLife().tick()
