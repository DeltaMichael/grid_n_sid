from time import sleep

def get_live_neighbors(grid, row, col):
    w = len(grid[0])
    h = len(grid)
    top = grid[row - 1][col] if row > 0 else 0
    bottom = grid[row + 1][col] if row < h else 0
    left = grid[row][col - 1] if col > 0 else 0
    right = grid[row][col + 1] if col < w else 0
    top_left = grid[row - 1][col - 1] if row > 0 and col > 0 else 0
    top_right = grid[row - 1][col + 1] if row > 0 and col < w else 0
    bottom_left = grid[row + 1][col - 1] if row < h and col > 0 else 0
    bottom_right = grid[row + 1][col + 1] if row < h and col < w else 0
    return top + bottom + left + right + top_left + top_right + bottom_left + bottom_right

def is_alive(grid, row, col):
    return grid[row][col] > 0

def generate(grid):
    w = len(grid[0])
    h = len(grid)
    next_gen = [[0 for _ in range(w)] for _ in range(h)]
    for i in range(h - 1):
        for j in range(w - 1):
            c = get_live_neighbors(grid, i, j)
            if is_alive(grid, i, j) and c < 2:
                next_gen[i][j] = 0
            if is_alive(grid, i, j) and c >= 2 and c <= 3:
                next_gen[i][j] = 1
            if is_alive(grid, i, j) and c > 3:
                next_gen[i][j] = 0
            if not is_alive(grid, i, j) and c == 3:
                next_gen[i][j] = 1
    return next_gen

# ANSI escape sequences
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
def hide_cursor():
    print('\033[?25l', end="")

# ANSI escape sequences
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
def cursorup(lines):
    print(f"\r\033[{lines}A", end="")

def lw_spaceship(grid, bl_r, bl_c):
    grid[bl_r - 3][bl_c + 1] = 1
    grid[bl_r - 3][bl_c + 4] = 1
    grid[bl_r - 2][bl_c] = 1
    grid[bl_r - 1][bl_c] = 1
    grid[bl_r][bl_c] = 1
    grid[bl_r][bl_c + 1] = 1
    grid[bl_r][bl_c + 2] = 1
    grid[bl_r][bl_c + 3] = 1
    grid[bl_r - 1][bl_c + 4] = 1

def blinker(grid, bl_r, bl_c):
    grid[bl_r][bl_c] = 1
    grid[bl_r][bl_c + 1] = 1
    grid[bl_r][bl_c + 2] = 1


def tick():

    GRID_H = 30
    GRID_W = 30
    grid = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]

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
        grepr = "\n".join([" ".join(map(lambda x: ' ' if x == 0 else '◼', row)) for row in grid])
        print(grepr)
        cursorup(GRID_H)
        grid = generate(grid)
        sleep(0.3)

tick()
