import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
# font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25) 

# reset

# reward

# play(action) -> direction

# game_iteration

# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', ['x','y'])

# BLOCKSIZE = 20
# SPEED = 1

# RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class SnakeGame:

    def __init__(self, width:int=640, height:int=480):
        self.width = width
        self.height = height
        self.speed = 20
        self.blocksize = 20
        
        #init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        #init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.width/2, self.height/2)
        self.snake = [
            self.head,
            Point(self.head.x-self.blocksize, self.head.y),
            Point(self.head.x-(2*self.blocksize), self.head.y)
        ]

        self.score = 0
        self.food = None
        self._place_food()

        self.frame_iteration = 0

    
    def _place_food(self):
        x = random.randint(0, (self.width - self.blocksize) // self.blocksize) * self.blocksize
        y = random.randint(0, (self.height - self.blocksize) // self.blocksize) * self.blocksize
        self.food = Point(x, y)
        # print(self.food.x, self.food.y, self.snake)
        if self.food in self.snake:
            self._place_food()
    
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, self.blocksize, self.blocksize))
            pygame.draw.rect(
                self.display, BLUE2, pygame.Rect(
                        pt.x+(self.blocksize*0.2), pt.y+(self.blocksize*0.2), self.blocksize*0.6, self.blocksize*0.6
                    )
                )
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, self.blocksize, self.blocksize))

        text = font.render(f'Score: {self.score}', True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    
    def _move(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_direction = clock_wise[((idx + 1) % 4)]
        elif np.array_equal(action, [0, 0, 1]):
            new_direction = clock_wise[((idx - 1) % 4)]
        
        self.direction = new_direction

        x = self.head.x 
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += self.blocksize
        elif self.direction == Direction.LEFT:
            x -= self.blocksize
        elif self.direction == Direction.DOWN:
            y += self.blocksize
        elif self.direction == Direction.UP:
            y -= self.blocksize
        
        self.head = Point(x, y)
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.width - self.blocksize or pt.x < 0 or pt.y > self.height - self.blocksize or pt.y < 0:
            return True

        # hit itself
        if pt in self.snake[1:]:
            return True
        return False
    
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect the user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         self.direction = Direction.LEFT
            #     elif event.key == pygame.K_RIGHT:
            #         self.direction = Direction.RIGHT
            #     elif event.key == pygame.K_DOWN:
            #         self.direction = Direction.DOWN
            #     elif event.key == pygame.K_UP:
            #         self.direction = Direction.UP
        

        # 2. move
        self._move(action)
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            # self.speed +=1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.speed)

        # 6. return if game over and score
        return reward, game_over, self.score

if __name__ == '__main__':
    game = SnakeGame()

    #game loop
    while True:
        reward, game_over, score = game.play_step()

        if game_over == True:
            break
    
    print(f'Reward: {reward} | Game Over: {game_over} | Score: {score}')
    pygame.quit()