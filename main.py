import pygame
import sys
import random
from game import Game2048
from models import Model1, normal_init, perturb_weights

import torch

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
TILE_SIZE = WIDTH // 4
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
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")
clock = pygame.time.Clock()

def draw_grid(grid):
    screen.fill(BACKGROUND_COLOR)
    for row in range(4):
        for col in range(4):
            value = grid[row][col]
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

def main():
    game = Game2048()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.slide_left()
                elif event.key == pygame.K_RIGHT:
                    game.slide_right()
                elif event.key == pygame.K_UP:
                    game.slide_up()
                elif event.key == pygame.K_DOWN:
                    game.slide_down()

        # Get game state and score
        state = game.get_state()
        score = game.get_score()

        # Print state and score for debugging
        print("State:")
        for row in state:
            print(row)
        print(f"Score: {score}")

        # Check for game-over conditions
        if game.is_game_over():
            print("Game Over!")
            running = False
        if game.has_won():
            print("You Win!")
            running = False

        # Draw the grid and update display
        draw_grid(state)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    #main()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    models = [Model1() for _ in range(100)]
    for model in models:
        model.apply(normal_init)

    EPOCHS = 1000
    for epoch in range(EPOCHS):
        scores = []
        for model in models:
            game = Game2048()
            running = True

            last_score = 0
            while running:
                state = game.get_state()
                state = torch.tensor(state).float()
                state = torch.clamp(state, min=1/2**10)
                state = torch.log2(state) - 3

                output = model(state)
                #print(output)
                action_id = torch.argmax(output).item()
                if action_id == 0:
                    game.slide_left()
                elif action_id == 1:
                    game.slide_up()
                elif action_id == 2:
                    game.slide_right()
                elif action_id == 3:
                    game.slide_down()

                if last_score == game.get_score():
                    functions = [game.slide_left, game.slide_up, game.slide_right, game.slide_down]
                    # Randomly select and call a function
                    selected_function = random.choice(functions)
                    selected_function()

                # Check for game-over conditions
                if game.is_game_over() or game.has_won():
                    scores.append(game.get_score())
                    #print(game.get_score())
                    running = False

                last_score = game.get_score()

        sorted_pairs = sorted(zip(scores, models), key=lambda x: x[0], reverse=True)
        sorted_scores, sorted_models = zip(*sorted_pairs)

        spawned_variations = []
        for model in models[:15]:
            for _ in range(5):  # Generate 5 variations per model
                spawned_variations.append(perturb_weights(model, std_dev=0.01))

        # Step 3: Add 10 completely new random models
        random_models = [Model1() for _ in range(10)]

        final_models = models[:15] + spawned_variations + random_models

        print(f"Epoch: {epoch+1}, top_score: {sorted_scores[0]}")