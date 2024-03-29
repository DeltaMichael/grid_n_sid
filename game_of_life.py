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

def get_live_neighbors(grid, r, c):
    cells = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
    values = [grid.get_cell_value(cell) for cell in cells]
    return sum(values)

# def get_live_neighbors(grid, row, col):
#     w = len(grid[0])
#     h = len(grid)
#     top = grid[row - 1][col] if row > 0 else 0
#     bottom = grid[row + 1][col] if row < h else 0
#     left = grid[row][col - 1] if col > 0 else 0
#     right = grid[row][col + 1] if col < w else 0
#     top_left = grid[row - 1][col - 1] if row > 0 and col > 0 else 0
#     top_right = grid[row - 1][col + 1] if row > 0 and col < w else 0
#     bottom_left = grid[row + 1][col - 1] if row < h and col > 0 else 0
#     bottom_right = grid[row + 1][col + 1] if row < h and col < w else 0
#     return top + bottom + left + right + top_left + top_right + bottom_left + bottom_right

def is_alive(grid, r, c):
    return grid.get_cell_value((r, c)) == 1

# def generate(grid):
#     w = len(grid[0])
#     h = len(grid)
#     next_gen = [[0 for _ in range(w)] for _ in range(h)]
#     for i in range(h - 1):
#         for j in range(w - 1):
#             c = get_live_neighbors(grid, i, j)
#             if is_alive(grid, i, j) and c < 2:
#                 next_gen[i][j] = 0
#             if is_alive(grid, i, j) and c >= 2 and c <= 3:
#                 next_gen[i][j] = 1
#             if is_alive(grid, i, j) and c > 3:
#                 next_gen[i][j] = 0
#             if not is_alive(grid, i, j) and c == 3:
#                 next_gen[i][j] = 1
#     return next_gen

def next_state(grid):
    ng_alive = []
    ng_dead = []
    for i in range(grid._h):
        for j in range(grid._w):
            n = get_live_neighbors(grid, i, j)
            if is_alive(grid, i, j) and n < 2:
                ng_dead.append((i, j))
            if is_alive(grid, i, j) and n >= 2 and n <= 3:
                ng_alive.append((i, j))
            if is_alive(grid, i, j) and n > 3:
                ng_dead.append((i, j))
            if not is_alive(grid, i, j) and n == 3:
                ng_alive.append((i, j))
    return ng_alive, ng_dead

# ANSI escape sequences
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
def hide_cursor():
    print('\033[?25l', end="")

# ANSI escape sequences
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
def cursorup(lines):
    print(f"\r\033[{lines}A", end="")

def lw_spaceship(grid, bl_r, bl_c):
    cells = [(bl_r - 3, bl_c + 1), (bl_r - 3, bl_c + 4), (bl_r - 2, bl_c), (bl_r - 1, bl_c), (bl_r, bl_c), (bl_r, bl_c + 1), (bl_r, bl_c + 2), (bl_r, bl_c + 3), (bl_r - 1, bl_c + 4)]
    grid.set_cells(cells)

def blinker(grid, bl_r, bl_c):
    cells = [(bl_r, bl_c), (bl_r, bl_c + 1), (bl_r, bl_c + 2)]
    grid.set_cells(cells)

def tick():
    grid = Grid(30, 30)
    blinker(grid, 4, 4)
    blinker(grid, 8, 4)
    blinker(grid, 12, 4)
    blinker(grid, 16, 4)
    blinker(grid, 20, 4)
    blinker(grid, 24, 4)
    lw_spaceship(grid, 5, 5)
    lw_spaceship(grid, 10, 10)
    lw_spaceship(grid, 15, 15)
    lw_spaceship(grid, 25, 25)
    hide_cursor()
    while(True):
        print(grid)
        cursorup(30)
        alive, dead = next_state(grid)
        grid.clear_cells(dead)
        grid.set_cells(alive)
        sleep(0.3)

tick()
