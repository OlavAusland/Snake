import random
from modules import cmd
import time
import sys

class Grid:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.board = {}

        cmd.Window.clear()
        for x in range(self.rows):
            for y in range(self.columns):
                cmd.Color.reset
                cmd.Color.cyan

                self.board[x, y] = '.'

    def draw(self):
        cmd.Window.clear()
        graphics = str()
        for index, (key, value) in enumerate(self.board.items()):
            if(index % self.columns == 0):
                graphics += '\n'

            print(value, end=" ")
            graphics += f'{value} '
        print(graphics, file=sys.stdout.flush())


class Apple:
    def __init__(self, grid):
        self.grid = grid
        self.symbol = cmd.Color.red + '●' + cmd.Color.reset
        self.position = (
            random.randint(0, grid.rows),
            random.randint(0, grid.columns)
        )

    def instantiate(self):
        self.grid.board[
            random.randint(0, self.grid.columns),
            random.randint(0, self.grid.rows)
        ] = self.symbol


class Snake:
    def __init__(self, grid):
        self.points = 0
        self.grid = grid
        self.symbol = '■'
        self.directions = self.directions = {'left':[0, -1], 'right':[0, 1], 'up':[-1, 0], 'down':[1, 0]}

        self.body = [
            (10, 10)
        ]

    def clear(self):
        cmd.Window.clear()
        for key, value in self.grid.board.items():
            for point in self.body:
                if(point == key):
                    self.grid.board[key] = '.'

    def update(self):
        self.clear()
        for key, value in self.grid.board.items():
            for point in self.body:
                if(point == key):
                    self.grid.board[key] = self.symbol

    def move(self, direction):
        for index, point in enumerate(self.body):
            point = (point[0] + direction[0], point[1] + direction[1])

        self.update()



grid = Grid(20, 20)
snake = Snake(grid)
apple = Apple(grid)

apple.instantiate()
for i in range(10):
    snake.move(snake.directions[random.choice(['left', 'right', 'up', 'down'])])
    grid.draw()
    time.sleep(1)
