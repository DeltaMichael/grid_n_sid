from snid.grid_game import GridGame

class GameOfLife(GridGame):

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