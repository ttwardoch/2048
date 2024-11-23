import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 6
TILE_SIZE = WIDTH // GRID_SIZE
PADDING = 10
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2024: (237, 194, 46),
}
TEXT_COLOR = (119, 110, 101)
FONT = pygame.font.Font(None, 50)
FPS = 1

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")
clock = pygame.time.Clock()


class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.spawn_tile()
        self.spawn_tile()

    def draw_grid(self):
        screen.fill(BACKGROUND_COLOR)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = self.grid[row][col]
                color = TILE_COLORS.get(value, TILE_COLORS[2024])
                pygame.draw.rect(
                    screen,
                    color,
                    (
                        col * TILE_SIZE + PADDING,
                        row * TILE_SIZE + PADDING,
                        TILE_SIZE - PADDING * 2,
                        TILE_SIZE - PADDING * 2,
                    ),
                    0,
                )
                if value > 0:
                    text = FONT.render(str(value), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(
                        col * TILE_SIZE + TILE_SIZE // 2,
                        row * TILE_SIZE + TILE_SIZE // 2,
                    ))
                    screen.blit(text, text_rect)

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
        return any(2048 in row for row in self.grid) or any(4096 in row for row in self.grid)

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


def main():
    game = Game2048()
    running = True

    while running:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             game.slide_left()
        #         elif event.key == pygame.K_RIGHT:
        #             game.slide_right()
        #         elif event.key == pygame.K_UP:
        #             game.slide_up()
        #         elif event.key == pygame.K_DOWN:
        #             game.slide_down()

        time.sleep(0.005)
        game.slide_left()
        time.sleep(0.005)
        game.slide_down()
        time.sleep(0.005)
        game.slide_right()
        time.sleep(0.005)
        game.slide_up()

        # Get the state and score
        state = game.get_state()
        score = game.get_score()

        # Print state and score for debugging
        print("Grid State:")
        for row in state:
            print(row)
        print(f"Score: {score}")

        if game.is_game_over():
            print("Game Over!")
            running = False
        if game.has_won():
            print("You Win!")
            running = False

        game.draw_grid()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()