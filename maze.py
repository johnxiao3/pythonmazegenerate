###################################
# Python maze generator program
# using PyGame for animation
# Davis MT
# Python 3.4
# 10.02.2018
###################################

import pygame
import time
import random
import os
from PIL import Image
from pypdf import PdfMerger

# setup maze variables
TOT_MAZES = 20
CELL_W = 40
TOT_R = 12
TOT_C = 12
LINE_W = 4

#-------------------------
grid = []
visited = []
stack = []
solution = {}

# set up pygame window
WIDTH = CELL_W*(TOT_C+2)
HEIGHT = CELL_W*(TOT_R+2)
FPS = 30

# Define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)

# initalise Pygame
pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1000,45)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Initializing RGB Color 
screen.fill(WHITE)
pygame.init()
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()




# build the grid
def build_grid(x, y, w):
    x0,y0 = x,y
    for i in range(1,TOT_R+1):
        x = CELL_W                                                            # set x coordinate to start position
        y = y + CELL_W                                                        # start a new row
        for j in range(1, TOT_C+1):
            pygame.draw.line(screen, BLACK, [x, y], [x + CELL_W, y],width=LINE_W)           # top of cell
            pygame.draw.line(screen, BLACK, [x + CELL_W, y], [x + CELL_W, y + CELL_W],width=LINE_W)   # right of cell
            pygame.draw.line(screen, BLACK, [x + CELL_W, y + w], [x, y + CELL_W],width=LINE_W)   # bottom of cell
            pygame.draw.line(screen, BLACK, [x, y + CELL_W], [x, y],width=LINE_W)           # left of cell
            grid.append((x,y))                                            # add cell to grid list
            x = x + CELL_W                                                    # move cell to new position
    pygame.draw.line(screen, WHITE, [x0-CELL_W, y0+CELL_W], [x0-CELL_W, y0+2*CELL_W],width=LINE_W)           # top of cell

    pygame.draw.line(screen, WHITE, [x, y], [x, y+CELL_W],width=LINE_W)           # top of cell

def push_up(x, y):
    pygame.draw.rect(screen, WHITE, (x + 1+LINE_W, y - CELL_W + 1+LINE_W, CELL_W-2-LINE_W, CELL_W*2-2-LINE_W), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, WHITE, (x +  1+LINE_W, y + 1+LINE_W, CELL_W-2-LINE_W, CELL_W*2-2-LINE_W), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, WHITE, (x - CELL_W +1+LINE_W, y+1+LINE_W, CELL_W*2-2-LINE_W, CELL_W-2-LINE_W), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, WHITE, (x +1+LINE_W, y +1+LINE_W, CELL_W*2-2-LINE_W, CELL_W-2-LINE_W), 0)
    pygame.display.update()


def single_cell( x, y):
    pygame.draw.rect(screen, GREEN, (x +1+LINE_W, y +1+LINE_W, CELL_W-2-LINE_W, CELL_W-2-LINE_W), 0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, WHITE, (x +1+LINE_W, y +1+LINE_W, CELL_W-2-LINE_W, CELL_W-2-LINE_W), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                        # has visited cell


def solution_cell(x,y):
    pygame.draw.rect(screen, YELLOW, (x+8, y+8, 5, 5), 0)             # used to show the solution
    pygame.display.update()                                        # has visited cell


def carve_out_maze(x,y):
    single_cell(x, y)                                              # starting positing of maze
    stack.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        #time.sleep(.07)                                            # slow program now a bit
        cell = []                                                  # define cell list
        if (x + CELL_W, y) not in visited and (x + CELL_W, y) in grid:       # right cell available?
            cell.append("right")                                   # if yes add to cell list

        if (x - CELL_W, y) not in visited and (x - CELL_W, y) in grid:       # left cell available?
            cell.append("left")

        if (x , y + CELL_W) not in visited and (x , y + CELL_W) in grid:     # down cell available?
            cell.append("down")

        if (x, y - CELL_W) not in visited and (x , y - CELL_W) in grid:      # up cell available?
            cell.append("up")

        if len(cell) > 0:                                          # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly

            if cell_chosen == "right":                             # if this cell has been chosen
                push_right(x, y)                                   # call push_right function
                solution[(x + CELL_W, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + CELL_W                                          # make this cell the current cell
                visited.append((x, y))                              # add to visited list
                stack.append((x, y))                                # place current cell on to stack

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - CELL_W, y)] = x, y
                x = x - CELL_W
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x , y + CELL_W)] = x, y
                y = y + CELL_W
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x , y - CELL_W)] = x, y
                y = y - CELL_W
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            #time.sleep(.05)                                       # slow program down a bit
            backtracking_cell(x, y)                               # change colour to green to identify backtracking path

def plot_route_back(x,y):
    solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (TOT_R,TOT_C):                                     # loop until cell position == start position
        x, y = solution[x, y]                                    # "key value" now becomes the new key
        solution_cell(x, y)                                      # animate route back
        time.sleep(.1)


for page in range(TOT_MAZES):
    grid = []
    visited = []
    stack = []
    solution = {}
    screen.fill(WHITE)
    pygame.display.update() 
    x, y = CELL_W, CELL_W                     # starting position of grid
    build_grid(CELL_W*2, 0, CELL_W)             # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
    carve_out_maze(x,y)               # call build the maze  function
    pygame.image.save(screen, str(page) + ".png")
    pygame.display.update() 
    print(page)


pdfs = []
for page in range(TOT_MAZES):
    print(page)
    img1 = Image.open(str(page) + ".png")
    im_1 = img1.convert('RGB')
    im_1.save(str(page) + ".pdf")
    pdfs.append(str(page) + ".pdf")

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()


print('completed !...')


'''
plot_route_back(w*x, w*y)         # call the plot solution function
# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
'''
