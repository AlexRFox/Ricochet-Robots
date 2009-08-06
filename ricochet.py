#! /usr/bin/env python

import pygame, sys, re
from pygame.locals import *

class Square:
    def __init__ (self, img, coords,
                  left = None, right = None, up = None, down = None):
        self.img = img
        self.coords = coords
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.box = pygame.Rect (coords[0] * 40, coords[1] * 40, 40, 40)

def draw ():
    screen.fill ((0xff, 0xff, 0xff))
    
    for row in grid:
        for square in row:
            screen.blit (square.img, (square.coords[0] * 40,
                                      square.coords[1] * 40))

    for row in grid:
        for square in row:
            if not square.right:
                pygame.draw.line (screen, (0xff, 0x0, 0x0),
                                  (square.coords[0] * 40 + 40 - 1,
                                   square.coords[1] * 40),
                                  (square.coords[0] * 40 + 40 - 1,
                                   square.coords[1] * 40 + 40),
                                  2)
            if not square.left:
                pygame.draw.line (screen, (0xff, 0x0, 0x0),
                                  (square.coords[0] * 40,
                                   square.coords[1] * 40),
                                  (square.coords[0] * 40,
                                   square.coords[1] * 40 + 40),
                                  2)
            if not square.up:
                pygame.draw.line (screen, (0xff, 0x0, 0x0),
                                  (square.coords[0] * 40,
                                   square.coords[1] * 40),
                                  (square.coords[0] * 40 + 40 - 1,
                                   square.coords[1] * 40),
                                  2)
            if not square.down:
                pygame.draw.line (screen, (0xff, 0x0, 0x0),
                                  (square.coords[0] * 40,
                                   square.coords[1] * 40 + 40),
                                  (square.coords[0] * 40 + 40,
                                   square.coords[1] * 40 + 40),
                                  2)

    if selected:
        pygame.draw.rect (screen, (0xff, 0xff, 0x0), selected.box, 3)

        if selected.left:
            pygame.draw.rect (screen, (0x0, 0x0, 0xff), selected.left.box, 2)
        if selected.right:
            pygame.draw.rect (screen, (0x0, 0x0, 0xff), selected.right.box, 2)
        if selected.up:
            pygame.draw.rect (screen, (0x0, 0x0, 0xff), selected.up.box, 2)
        if selected.down:
            pygame.draw.rect (screen, (0x0, 0x0, 0xff), selected.down.box, 2)

def gengrid ():
    grid = []
    for x in range (16):
        grid += [[]]
        for y in range (16):
            grid[x] += [Square (squareimg, (x, y))]

    for x in range (16):
        for y in range (16):
            if grid[x][y].coords[0] != 0:
                grid[x][y].left = grid[x-1][y]
            if grid[x][y].coords[0] != 15:
                grid[x][y].right = grid[x+1][y]
            if grid[x][y].coords[1] != 0:
                grid[x][y].up = grid[x][y-1]
            if grid[x][y].coords[1] != 15:
                grid[x][y].down = grid[x][y+1]

    grid = mkwalls (grid)

    return grid

def mkwalls (grid):
    file = open ("first.map")
    line = file.readline ()
    while line != "":
        coords = re.findall (r'[0-9]*', line)
        data = []
        for num in coords:
            if num != '':
                data.append (int (num))

        coords = data[:2]
        print data
        print coords

        cursquare = grid[coords[0]][coords[1]]

        if data[2]:
            if cursquare.left:
                cursquare.left.right = None
                cursquare.left = None
        if data[3]:
            if cursquare.right:
                cursquare.right.left = None
                cursquare.right = None
        if data[4]:
            if cursquare.up:
                cursquare.up.down = None
                cursquare.up = None
        if data[5]:
            if cursquare.down:
                cursquare.down.up = None
                cursquare.down = None
            
        line = file.readline ()

    return grid

pygame.init ()

screen = pygame.display.set_mode ((642, 642))
pygame.display.set_caption ('Ricochet Robots')

squareimg = pygame.image.load ("./square.png")

grid = gengrid ()

mousepos = pygame.mouse.get_pos ()

selected = None

while True:
    for event in pygame.event.get ():
        if event.type == QUIT:
            sys.exit ()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit ()
        elif event.type == MOUSEMOTION:
            mousepos = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            for row in grid:
                for square in row:
                    if square.box.collidepoint (mousepos):
                        selected = square

    draw ()
    pygame.display.flip ()
