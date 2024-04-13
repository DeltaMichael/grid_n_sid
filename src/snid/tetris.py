from snid.grid_game import GridGame
from random import choice


class Tetris(GridGame):

    def tetrimo(self):
        self._cur_tetrimo = choice(self._all_tetrimos)
        self._grid.set_cells(self._cur_tetrimo)

    def _bottom_edge(self):
        bottom_row = max(self._cur_tetrimo)
        edge = [(y, x) for y, x in self._cur_tetrimo if y == bottom_row[0]]
        return edge

    def _collision(self):
        for y, x in self._bottom_edge():
            if not self._grid._is_cell_valid(y + 1, x):
                return True
            if self._grid.get_cell_value((y + 1, x)):
                return True
        return False

    def _move_tetrimo_down(self):
        self._grid.clear_cells(self._cur_tetrimo)
        self._cur_tetrimo = [(y + 1, x) for y, x in self._cur_tetrimo]
        self._grid.set_cells(self._cur_tetrimo)

    def _init_state(self):
        mid = self._grid._w // 2
        self._all_tetrimos = [
            [(0, mid), (1, mid), (1, mid - 1), (1, mid + 1)], [(0, mid), (1, mid), (1, mid - 1), (2, mid)], [(0, mid), (1, mid), (1, mid + 1), (2, mid)], [(0, mid), (0, mid + 1), (0, mid - 1), (0, mid - 2)], [(0, mid), (1, mid), (2, mid), (3, mid)]]
        self.tetrimo()

    def _update_state(self):
        if self._collision():
            self.tetrimo()
        else:
            self._move_tetrimo_down()
