import random
import time

import pygame as pg

COLORS = {"red": (255, 0, 0), "cyan": (0, 255, 255), "white": (255, 255, 255), 'yellow': (255, 255, 0),
          "black": (0, 0, 0)}
CELL_SIZE = (10, 10)
WINDOW_WIDTH = 800
SURFACE_WIDTH = WINDOW_WIDTH - 100
WINDOW_HEIGHT = 600
SURFACE_HEIGHT = WINDOW_HEIGHT - 100
INIT_SNAKE_SPEED = 10


class SnakeGame:

    def __init__(self):
        self.snake_speed = INIT_SNAKE_SPEED

        self.snake_head_pos = [int(round(SURFACE_WIDTH / 2, -1)),
                               int(round(SURFACE_WIDTH / 2, -1))]  # Initial snake's position, which changes in game
        self.snake_parts = [self.snake_head_pos]
        self.food_pos = self._food_gen()

        self.game_is_over = False
        self.game_close = False

        self.font_style_game_over = pg.font.SysFont("Avenir", 50, True)
        self.font_style_replay = pg.font.SysFont("Arial", 20, True)
        self.font_style_score = pg.font.SysFont("comicsansms", 35, True)

    def run_game(self):

        window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        gaming_surface = pg.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))

        pg.display.set_caption("Snake Game")

        x_diff = 0
        y_diff = 0

        score = len(self.snake_parts) - 1

        clock = pg.time.Clock()

        while not self.game_is_over:

            while self.game_close:

                window.fill(COLORS["white"])
                self._message('You Lost! Press q-Quit or r-Play Again', COLORS["red"], window, self.font_style_replay)
                pg.display.flip()

                for event in pg.event.get():

                    if event.type == pg.QUIT:
                        self.game_is_over = True
                        self.game_close = False

                    if event.type == pg.KEYDOWN:  # quit o restart the game
                        if event.key == pg.K_q:
                            self.game_is_over = True
                            self.game_close = False
                        elif event.key == pg.K_r:
                            self.game_close = False
                            self.snake_head_pos = [round(SURFACE_WIDTH / 2, -1), round(SURFACE_WIDTH / 2, -1)]
                            self.snake_parts = [self.snake_head_pos]
                            self.snake_speed = INIT_SNAKE_SPEED
                            self.food_pos = self._food_gen()
                            self.run_game()

            # get movement action or quit game after pressing X
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_is_over = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        x_diff = -10
                        y_diff = 0
                    elif event.key == pg.K_RIGHT:
                        x_diff = 10
                        y_diff = 0
                    elif event.key == pg.K_UP:
                        x_diff = 0
                        y_diff = -10
                    elif event.key == pg.K_DOWN:
                        x_diff = 0
                        y_diff = 10

            # enumerates reversed list and changes pos of every element
            for index, part in list(enumerate(self.snake_parts))[::-1]:

                if part == self.snake_parts[0]:
                    part[0] += x_diff
                    part[1] += y_diff
                else:
                    self.snake_parts[index][0] = self.snake_parts[index-1][0]
                    self.snake_parts[index][1] = self.snake_parts[index - 1][1]

            #  checks if snake is inside borders
            if self.snake_head_pos[0] > SURFACE_WIDTH - CELL_SIZE[0] or self.snake_head_pos[0] < 0 \
                    or self.snake_head_pos[1] > SURFACE_HEIGHT - CELL_SIZE[1] or self.snake_head_pos[1] < 0:
                self.game_close = True

            for part in self.snake_parts[1:]:
                if self.snake_head_pos == part:
                    self.game_close = True

            gaming_surface.fill(COLORS["white"])
            window.fill(COLORS['black'])

            #  indicates snake
            for part in self.snake_parts:
                pg.draw.rect(gaming_surface, COLORS['red'], [part, CELL_SIZE])

            #  indicates food
            pg.draw.rect(gaming_surface, COLORS['cyan'], [self.food_pos, CELL_SIZE])

            #  indicates score
            self._message(f'Score {len(self.snake_parts)-1}', COLORS["yellow"], window, self.font_style_score, (30, 5))

            #  increases snake's length when it eats
            if self.food_pos == tuple(self.snake_head_pos):
                self.food_pos = self._food_gen()
                new_cell_x = self.snake_parts[-1][0] - x_diff
                new_cell_y = self.snake_parts[-1][1] - y_diff
                self.snake_parts.append([new_cell_x, new_cell_y])

            window.blit(gaming_surface, ((WINDOW_HEIGHT- SURFACE_HEIGHT)/2,
                                         (WINDOW_WIDTH-SURFACE_WIDTH)/2))

            pg.display.flip()

            clock.tick(self.snake_speed)

        window.fill(COLORS["white"])
        self._message('Game Over', COLORS["red"], window, self.font_style_game_over)
        pg.display.update()
        time.sleep(3)

        pg.quit()

    def _food_gen(self):
        """This method randomly generates food"""
        food_x = round(random.randrange(0, SURFACE_WIDTH - CELL_SIZE[0]), -1)
        food_y = round(random.randrange(0, SURFACE_HEIGHT - CELL_SIZE[1]), -1)
        return food_x, food_y

    def _message(self, msg, color, surface, font, position=None):
        """
        This method indicates messages on a given surfaces
        """
        mesg = font.render(msg, True, color)
        if position is None:
            text_rect = mesg.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2))
            surface.blit(mesg, text_rect)
        else:
            surface.blit(mesg, position)


if __name__ == "__main__":
    pg.init()
    game = SnakeGame()
    game.run_game()
    quit()
