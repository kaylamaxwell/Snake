import pygame as pg
from random import randrange


class GUI:
    def __init__(self):
        pg.init()

        self.WINDOW = 1000
        self.TILE_SIZE = 50
        self.RANGE = (self.TILE_SIZE // 2, self.WINDOW - self.TILE_SIZE // 2, self.TILE_SIZE)
        self.get_random_position = lambda: [randrange(*self.RANGE), randrange(*self.RANGE)]
        self.snake = pg.Rect(0, 0, self.TILE_SIZE - 2, self.TILE_SIZE - 2)
        self.snake.center = self.get_random_position()
        self.length = 1
        self.segments = [self.snake.copy()]
        self.snake_dir = (0, 0)
        self.time_step = 110
        self.time = 0
        self.food = self.snake.copy()
        self.food.center = self.get_random_position()
        self.screen = pg.display.set_mode((self.WINDOW, self.WINDOW))
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("cambria", 36)
        self.dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

        # Define game states
        self.START_SCREEN = 0
        self.GAMEPLAY = 1
        self.END_SCREEN = 2

        self.game_state = self.START_SCREEN
        self.current_score = 0
        self.high_score = 0

        # Load high score from file
        self.load_high_score()

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def show_start_screen(self):
        self.screen.fill((0, 0, 0))

        # Render and display the game title
        title_text = self.font.render("Snake Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.WINDOW // 2, 100))
        self.screen.blit(title_text, title_rect)

        # Current high score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(self.WINDOW // 2, 200))
        self.screen.blit(high_score_text, high_score_rect)

        # Game instructions
        instruction_text = ("Use WSAD to control the snake. Eat food to increase your size "
                            "without running into the walls or eating yourself")

        # Split the instruction text into wrapped lines
        wrapped_lines = []
        max_width = self.WINDOW - 100  # Maximum width for wrapped text
        words = instruction_text.split()
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + " " + word
            if self.font.size(test_line)[0] > max_width:
                wrapped_lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        wrapped_lines.append(current_line)

        # Display the wrapped instruction text
        y_offset = 300
        for line in wrapped_lines:
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.WINDOW // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += self.font.get_height() + 10  # Adjust the vertical spacing

        # Display start game prompt
        start_text = self.font.render("Press SPACE to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.WINDOW // 2, y_offset + 20))
        self.screen.blit(start_text, start_rect)

        pg.display.flip()

        # Wait for SPACE key press to start the game
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    waiting = False

    def show_end_screen(self):
        self.screen.fill((0, 0, 0))

        # Display game over text
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)

        # Display player's score and high score
        stats_text = self.font.render(f"Score: {self.current_score}  High Score: {self.high_score}", True,
                                      (255, 255, 255))
        stats_rect = stats_text.get_rect(center=(self.WINDOW // 2, 300))
        self.screen.blit(stats_text, stats_rect)

        # Restart and quit options
        restart_text = self.font.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.WINDOW // 2, 400))
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font.render("Press Q to Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(self.WINDOW // 2, 450))
        self.screen.blit(quit_text, quit_rect)

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

    def restart_game(self):
        self.current_score = 0
        self.snake.center = self.get_random_position()
        self.segments = [self.snake.copy()]
        self.snake_dir = (0, 0)
        self.length = 1
        self.food.center = self.get_random_position()
        self.game_state = self.START_SCREEN  # Reset game state to start screen

        running = True
        while running:
            if self.game_state == self.START_SCREEN:
                self.show_start_screen()
                self.game_state = self.GAMEPLAY  # Go to gameplay when player starts

            elif self.game_state == self.GAMEPLAY:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    # Player input during gameplay
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_w and self.dirs[pg.K_w]:
                            self.snake_dir = (0, -self.TILE_SIZE)
                            self.dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                        if event.key == pg.K_s and self.dirs[pg.K_s]:
                            self.snake_dir = (0, self.TILE_SIZE)
                            self.dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                        if event.key == pg.K_a and self.dirs[pg.K_a]:
                            self.snake_dir = (-self.TILE_SIZE, 0)
                            self.dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                        if event.key == pg.K_d and self.dirs[pg.K_d]:
                            self.snake_dir = (self.TILE_SIZE, 0)
                            self.dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

                self.screen.fill((0, 0, 0))

                # Check borders and self eating
                self_eating = self.snake.collidelist(self.segments[:-1]) != -1
                if (self.snake.left < 0 or self.snake.right > self.WINDOW or
                        self.snake.top < 0 or self.snake.bottom > self.WINDOW or
                        self_eating):
                    self.game_state = self.END_SCREEN  # Transition to end screen

                # Check food
                if self.snake.center == self.food.center:
                    self.food.center = self.get_random_position()
                    self.length += 1
                    self.current_score += 1
                    if self.current_score > self.high_score:
                        self.high_score = self.current_score

                # Draw food
                pg.draw.rect(self.screen, (255, 0, 0), self.food)

                # Draw snake
                for segment in self.segments:
                    pg.draw.rect(self.screen, (0, 255, 0), segment)

                # Render and display scores
                score_text = self.font.render(f"Score: {self.current_score}  High Score: {self.high_score}", True,
                                              (255, 255, 255))
                self.screen.blit(score_text, (10, 10))

                # Move snake
                time_now = pg.time.get_ticks()
                if time_now - self.time > self.time_step:
                    self.time = time_now
                    self.snake.move_ip(self.snake_dir)
                    self.segments.append(self.snake.copy())
                    self.segments = self.segments[-self.length:]

            elif self.game_state == self.END_SCREEN:
                restart = self.show_end_screen()
                if restart:
                    self.restart_game()  # Reset game variables
                    self.game_state = self.START_SCREEN  # Go back to start screen
                else:
                    self.save_high_score()  # Save high score
                    running = False  # Quit

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()


# Create an instance of GUI and run the game
gui = GUI()
gui.restart_game()  # Start the game loop
