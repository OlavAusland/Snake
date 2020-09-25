import random
import time
import sys

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
        self.symbol = '■'
        self.body = [[4, 4], [4, 5], [4, 6]]
        self.grid = grid
        self.directions = ['left', 'right', 'up', 'down']

    def move(self, grid, direction):

        if(direction == 'left'):
            for index, point in enumerate(reversed(self.body)):
                try:
                    self.body[index] = self.body[index - 1]
                except Exception as error:
                    print(error)
                    self.body[index] = [point[0] - 1, point[1]]



class Apple:
    def __init__(self):
        pass

class GameManager:
    def __init__(self, grid, snake, apple):
        self.grid = grid
        self.snake = snake
        self.apple = apple
        self.score = 0

    def update(self):
        layout = str()

        self.snake.move(self.grid, 'left')
        for index, point in enumerate(self.grid.layout):
            if(index % self.grid.columns == 0 and index != 0):
                layout += '\n'
            if(point == self.snake.body[0] or point == self.snake.body[1]):
                layout += 'X '
            else:
                layout += '. '
        layout += '\n'
        print(layout, end=None, file=sys.stdout.flush())


def main():
    grid = Grid(10, 10)
    snake = Snake(grid)
    apple = Apple()
    gameManager = GameManager(grid, snake, apple)
    for _ in range(4):
        gameManager.update()
        time.sleep(1)

if __name__ == '__main__':
    main()
