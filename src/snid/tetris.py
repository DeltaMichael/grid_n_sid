from snid.grid_game import GridGame
from random import choice
from keyboard import add_hotkey


class Tetrimo:

    def rotate(self):
        pass


class T(Tetrimo):

    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.offset = 0

        '''
        ***
         *

         *
        **
         *

         *
        ***

         *
         **
         *
        '''
        self._variant = choice([0, 1, 2, 3])
        self._variants = [[(y, x), (y, x + 1), (y, x - 1), (y + 1, x)],
                          [(y, x), (y + 1, x), (y + 1, x - 1), (y + 2, x)],
                          [(y, x), (y + 1, x + 1), (y + 1, x - 1), (y + 1, x)],
                          [(y, x), (y + 1, x), (y + 1, x + 1), (y + 2, x)]]

        self._edge_variants = [[(y, x + 1), (y, x - 1), (y + 1, x)],
                               [(y + 1, x - 1), (y + 2, x)],
                               [(y + 1, x + 1), (y + 1, x - 1), (y + 1, x)],
                               [(y + 1, x + 1), (y + 2, x)]]

        self._cells = self._variants[self._variant]
        self._edges = self._edge_variants[self._variant]

    def bottom_edge(self):
        return self._edges

    def move_down(self):
        self.y = self.y + 1
        self._cells = [(y + 1, x) for y, x in self._cells]
        self._edges = [(y + 1, x) for y, x in self._edges]

    def move_left(self):
        self.x = self.x - 1
        self.offset -= 1
        self._cells = [(y, x - 1) for y, x in self._cells]
        self._edges = [(y, x - 1) for y, x in self._edges]

    def move_right(self):
        self.x = self.x + 1
        self.offset += 1
        self._cells = [(y, x + 1) for y, x in self._cells]
        self._edges = [(y, x + 1) for y, x in self._edges]

    def rotate(self):
        self._variant = (self._variant + 1) % 4
        self._cells = [(self.y + y, x + self.offset)
                       for y, x in self._variants[self._variant]]
        self._edges = [(self.y + y, x + self.offset)
                       for y, x in self._edge_variants[self._variant]]


class Tetris(GridGame):

    def tetrimo(self, y, x):
        self._template = choice(self._all_tetrimos)
        self._cur_tetrimo = self._template(y, x)
        self._grid.set_cells(self._cur_tetrimo._cells)

    def _collision(self):
        for y, x in self._cur_tetrimo.bottom_edge():
            if not self._grid._is_cell_valid(y + 1, x):
                return True
            if self._grid.get_cell_value((y + 1, x)) == 1:
                return True
        return False

    def _move_tetrimo_down(self):
        self._grid.clear_cells(self._cur_tetrimo._cells)
        self._cur_tetrimo.move_down()
        self._grid.set_cells(self._cur_tetrimo._cells)

    def _move_tetrimo_left(self):
        self._grid.clear_cells(self._cur_tetrimo._cells)
        self._cur_tetrimo.move_left()
        self._grid.set_cells(self._cur_tetrimo._cells)

    def _move_tetrimo_right(self):
        self._grid.clear_cells(self._cur_tetrimo._cells)
        self._cur_tetrimo.move_right()
        self._grid.set_cells(self._cur_tetrimo._cells)

    def _rotate_tetrimo(self):
        self._grid.clear_cells(self._cur_tetrimo._cells)
        self._cur_tetrimo.rotate()
        self._grid.set_cells(self._cur_tetrimo._cells)

    def _init_state(self):
        self._mid = self._grid._w // 2
        self._all_tetrimos = [T]
        add_hotkey(4, self._move_tetrimo_left)
        add_hotkey(37, self._move_tetrimo_right)
        add_hotkey('space', self._rotate_tetrimo)
        self.tetrimo(0, self._mid)

    def _update_state(self):
        if self._collision():
            self.tetrimo(0, self._mid)
        else:
            self._move_tetrimo_down()
