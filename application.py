import random
import time
import sys
import keyboard
from modules import cmd
from threading import Thread

class Grid:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.layout = []

        #Initialize grid
        for x in range(self.columns):
            for y in range(self.rows):
                self.layout.append([x, y])

class Snake:
    def __init__(self, grid):
        self.symbol = f'{cmd.Color.green}■{cmd.Color.reset}'
        self.body = [[4, 4], [4, 5], [4, 6], [4, 7], [4, 8]]
        self.ghost_pos = self.body[-1]
        self.grid = grid
        self.directions = ['left', 'right', 'up', 'down']

    def move(self, grid, direction):
        self.ghost_pos = self.body[-1]
        for i in range(len(self.body)-1,0,-1):
            self.body[i] = self.body[i-1]

        if(direction == 'left'):
            self.body[0] = [self.body[0][0], self.body[0][1] - 1]
            if(self.body[0][1] < 0):
                self.body[0][1] = self.grid.columns - 1
        if(direction == 'right'):
            self.body[0] = [self.body[0][0], self.body[0][1] + 1]
            if(self.body[0][1] > self.grid.columns - 1):
                self.body[0][1] = 0
        if(direction == 'up'):
            self.body[0] = [self.body[0][0] - 1, self.body[0][1]]
            if(self.body[0][0] < 0):
                self.body[0][0] = self.grid.rows - 1
        if(direction == 'down'):
            self.body[0] = [self.body[0][0] + 1, self.body[0][1]]
            if(self.body[0][0] >= self.grid.rows):
                self.body[0][0] = 0

class Apple:
    def __init__(self):
        self.symbol = f'{cmd.Color.red}●{cmd.Color.reset}'
        self.position = list()

    def instantiate(self, grid, snake):
        while True:
            self.position = [
                random.randint(1, grid.columns),
                random.randint(1, grid.rows)
            ]

            for point in snake.body:
                if(point == self.position):
                    self.instantiate()
            break

class GameManager:
    def __init__(self, grid, snake, apple):
        self.grid = grid
        self.snake = snake
        self.apple = apple
        self.score = 0

        self.apple.instantiate(self.grid, self.snake)

    def update(self, direction):
        cmd.Window.clear()
        layout = str()
        self.snake.move(self.grid, direction)
        if(self.isDead()):
            sys.exit()
        #CHANGE NAME
        for index, point in enumerate(self.grid.layout):
            if(index % self.grid.columns == 0 and index != 0):
                layout += '\n'
            if(point in self.snake.body):
                layout += f'{self.snake.symbol} '
                continue
            if(point == self.apple.position):
                layout += f'{self.apple.symbol} '
                continue
            layout += '. '
        layout += '\n'
        self.snake_score()
        print(layout, end=None, file=sys.stdout.flush())

    def snake_score(self):
        if(self.snake.body[0] == self.apple.position):
            self.score += 1
            self.snake.body.append(self.snake.ghost_pos)
            self.apple.instantiate(self.grid, self.snake)

    def isDead(self):
        for indexA, pointA in enumerate(self.snake.body):
            for indexB, pointB in enumerate(self.snake.body):
                if(pointA == pointB and indexA != indexB):
                    return True
        return False

direction = 'left'

def main():
    Thread(target=input).start()
    Thread(target=gameLoop).start()

def input():
    global direction
    while True:
        if(keyboard.is_pressed('w')):
            direction = 'up'
        elif(keyboard.is_pressed('a')):
            direction = 'left'
        elif(keyboard.is_pressed('s')):
            direction = 'down'
        elif(keyboard.is_pressed('d')):
            direction = 'right'
        time.sleep(0.01)

def gameLoop():
    global direction
    grid = Grid(25, 25)
    snake = Snake(grid)
    apple = Apple()
    gameManager = GameManager(grid, snake, apple)
    while True:
        gameManager.update(direction)
        if(gameManager.isDead()):
            break
        time.sleep(0.1)

if __name__ == '__main__':
    main()
