# https://www.youtube.com/watch?v=_-KjEgCLQFw

import pygame as pg
from random import randrange

WINDOW = 1000
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# Initialize pygame and font
pg.init()
font = pg.font.Font(None, 36)  # Change the font size as needed

# Define game states
START_SCREEN = 0
GAMEPLAY = 1
END_SCREEN = 2

game_state = START_SCREEN
current_score = 0
high_score = 0


# Load high score from file
def load_high_score():
    global high_score
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0


# Save high score to file
def save_high_score():
    global high_score
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))


# Initialize high score
load_high_score()


def show_start_screen():
    screen.fill('black')

    # Render and display the game title
    title_text = font.render("Snake Game", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW // 2, 100))
    screen.blit(title_text, title_rect)

    # Current high score
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect(center=(WINDOW // 2, 200))
    screen.blit(high_score_text, high_score_rect)

    # Game instructions
    instruction_text = ("Use WSAD to control the snake. Eat food to increase your size "
                        "without running into the walls or eating yourself")

    # Split the instruction text into wrapped lines
    wrapped_lines = []
    max_width = WINDOW - 100  # Maximum width for wrapped text
    words = instruction_text.split()
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + " " + word
        if font.size(test_line)[0] > max_width:
            wrapped_lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    wrapped_lines.append(current_line)

    # Display the wrapped instruction text
    y_offset = 300
    for line in wrapped_lines:
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WINDOW // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += font.get_height() + 10  # Adjust the vertical spacing

    # Display start game prompt
    start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(WINDOW // 2, y_offset + 20))
    screen.blit(start_text, start_rect)

    pg.display.flip()

    # Wait for SPACE key press to start the game
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                waiting = False


def show_end_screen():
    global high_score
    screen.fill('black')

    # Display game over text
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WINDOW // 2, 200))
    screen.blit(game_over_text, game_over_rect)

    # Display player's score and high score
    stats_text = font.render(f"Score: {current_score}  High Score: {high_score}", True, (255, 255, 255))
    stats_rect = stats_text.get_rect(center=(WINDOW // 2, 300))
    screen.blit(stats_text, stats_rect)

    # Restart and quit options
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WINDOW // 2, 400))
    screen.blit(restart_text, restart_rect)

    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(WINDOW // 2, 450))
    screen.blit(quit_text, quit_rect)

    pg.display.flip()

    # Wait for R or Q key press to restart or quit
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    waiting = False
                    return True  # Restart the game
                elif event.key == pg.K_q:
                    waiting = False
                    return False  # Quit the game


def restart_game():
    global current_score, snake, segments, snake_dir, length, food
    current_score = 0
    snake.center = get_random_position()
    segments = [snake.copy()]
    snake_dir = (0, 0)
    length = 1
    food.center = get_random_position()


running = True
while running:
    if game_state == START_SCREEN:
        show_start_screen()
        game_state = GAMEPLAY  # Go to gameplay when player starts

    elif game_state == GAMEPLAY:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # Player input during gameplay
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w and dirs[pg.K_w]:
                    snake_dir = (0, -TILE_SIZE)
                    dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_s and dirs[pg.K_s]:
                    snake_dir = (0, TILE_SIZE)
                    dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_a and dirs[pg.K_a]:
                    snake_dir = (-TILE_SIZE, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                if event.key == pg.K_d and dirs[pg.K_d]:
                    snake_dir = (TILE_SIZE, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

        screen.fill('black')

        # Check borders and self eating
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
            game_state = END_SCREEN  # Transition to end screen

        # Check food
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            current_score += 1
            if current_score > high_score:
                high_score = current_score

        # Draw food
        pg.draw.rect(screen, 'red', food)

        # Draw snake
        for segment in segments:
            pg.draw.rect(screen, 'green', segment)

        # Render and display scores
        score_text = font.render(f"Score: {current_score}  High Score: {high_score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Move snake
        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]

    elif game_state == END_SCREEN:
        restart = show_end_screen()
        if restart:
            restart_game()  # Reset game variables
            game_state = START_SCREEN  # Go back to start screen
        else:
            save_high_score()  # Save high score
            running = False  # Quit

    pg.display.flip()
    clock.tick(60)

pg.quit()
