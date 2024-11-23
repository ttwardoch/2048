import random

GRID_SIZE = 4


class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_tiles:
            row, col = random.choice(empty_tiles)
            self.grid[row][col] = random.choice([2, 4])

    def slide_row_left(self, row):
        new_row = [value for value in row if value != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [value for value in new_row if value != 0]
        return new_row + [0] * (GRID_SIZE - len(new_row))

    def slide_left(self):
        new_grid = [self.slide_row_left(row) for row in self.grid]
        if new_grid != self.grid:
            self.grid = new_grid
            self.spawn_tile()

    def rotate_grid(self):
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def slide_right(self):
        self.rotate_grid()
        self.rotate_grid()
        self.slide_left()
        self.rotate_grid()
        self.rotate_grid()

    def slide_up(self):
        self.rotate_grid()
        self.rotate_grid()
        self.rotate_grid()
        self.slide_left()
        self.rotate_grid()

    def slide_down(self):
        self.rotate_grid()
        self.slide_left()
        self.rotate_grid()
        self.rotate_grid()
        self.rotate_grid()

    def is_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False
            for i in range(GRID_SIZE - 1):
                if row[i] == row[i + 1]:
                    return False
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE - 1):
                if self.grid[row][col] == self.grid[row + 1][col]:
                    return False
        return True

    def has_won(self):
        return any(2024 in row for row in self.grid)

    def get_state(self):
        """
        Returns the current state of the grid as a 2D list of tiles.
        """
        return [row[:] for row in self.grid]

    def get_score(self):
        """
        Returns the total score, which is the sum of all tile values on the grid.
        """
        return sum(sum(row) for row in self.grid)