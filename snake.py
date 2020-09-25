import random
import time
import sys
import keyboard
from modules import cmd
from threading import Thread
import json

DATA = 'data.json'

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
        self.body = [[4, 4]]
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
                random.randint(1, grid.columns -1),
                random.randint(1, grid.rows -1)
            ]

            if(self.position in snake.body):
                    self.instantiate(grid, snake)
            break

class GameManager:
    global lost
    def __init__(self, grid, snake, apple):
        self.grid = grid
        self.snake = snake
        self.apple = apple
        self.score = 0

        self.apple.instantiate(self.grid, self.snake)

        #WINDOW NAME
        cmd.Window.title('Snake Game  I  Olav Ausland')
        #WINDOW SIZE
        cmd.Window.resize(50, 27)

    def update(self, direction):
        cmd.Window.clear()
        layout = str()
        self.snake.move(self.grid, direction)

        if(self.isDead()):
            if(self.score > self.request_high_score()):
                self.write_high_score(self.score)
            print(f'You Lost | Score: {self.score} | High Score: {self.request_high_score()}')
            lost = True
        else:
            print(f'Score: {self.score}')
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

    def request_high_score(self):
        with open(DATA, 'r+') as data:
            data = json.load(data)
            return data['High Score']

    def write_high_score(self, score):
        with open(DATA, 'w+') as file:
            data = {"High Score":score}
            json.dump(data, file)

direction = 'left'
lost = False

def main():
    Thread(target=input).start()
    Thread(target=gameLoop).start()

def input():
    global direction
    while not lost:
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
    while not lost:
        gameManager.update(direction)
        if(gameManager.isDead()):
            break
        time.sleep(0.1)

if __name__ == '__main__':
    main()
