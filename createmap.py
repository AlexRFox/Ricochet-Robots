#! /usr/bin/env python

import pygame, sys, re
from pygame.locals import *

class Square:
    def __init__ (self, img, coords,
                  left = None, right = None, up = None, down = None,
                  robot = None, symbol = None):
        self.img = img
        self.coords = coords
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.box = pygame.Rect (coords[0] * 40, coords[1] * 40, 40, 40)
        self.robot = robot
        self.symbol = symbol

class Robot:
    def __init__ (self, img, color, square = None):
        self.img = img
        self.color = color
        self.square = square

class Symbol:
    def __init__ (self, img, color, square = None):
        self.img = img
        self.color = color
        self.square = square

def draw ():
    screen.fill ((0xff, 0xff, 0xff))
    
    for row in grid:
        for square in row:
            screen.blit (square.img, (square.coords[0] * 40,
                                      square.coords[1] * 40))


    if red.square:
        screen.blit (red.img, (red.square.coords[0] * 40,
                               red.square.coords[1] * 40))
    if blue.square:
        screen.blit (blue.img, (blue.square.coords[0] * 40,
                                blue.square.coords[1] * 40))
    if green.square:
        screen.blit (green.img, (green.square.coords[0] * 40,
                                 green.square.coords[1] * 40))
    if yellow.square:
        screen.blit (yellow.img, (yellow.square.coords[0] * 40,
                                  yellow.square.coords[1] * 40))

    for color in symbols:
        for form in symbols[color]:
            if symbols[color][form].square:
                screen.blit (symbols[color][form].img,
                             (symbols[color][form].square.coords[0] * 40,
                              symbols[color][form].square.coords[1] * 40))

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

    grid = loadmap (grid)

    return grid

def loadmap (grid):
    #File line format: (x, y)
    # left right up down redbot bluebot greenbot yellowbot
    #  redbio redhex redtar redtri
    #  bluebio bluehex bluetar bluetri
    #  greenbio greenhex greentar greentri
    #  yellowbio yellowhex yellowtar yellowtri
    #   Example: (14, 10) 1 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

    file = open ("first.map")
    line = file.readline ()
    while line != "":
        coords = re.findall (r'[0-9]*', line)
        data = []
        for num in coords:
            if num != '':
                data.append (int (num))

        coords = data[:2]

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
        if data[6]:
            red.square = cursquare
            red.square.robot = red
        if data[7]:
            blue.square = cursquare
            blue.square.robot = blue
        if data[8]:
            green.square = cursquare
            green.square.robot = green
        if data[9]:
            yellow.square = cursquare
            yellow.square.robot = yellow
        if data[10]:
            symbols['red']['bio'].square = cursquare
            cursquare.symbol = symbols['red']['bio']
        if data[11]:
            symbols['red']['hex'].square = cursquare
            cursquare.symbol = symbols['red']['hex']
        if data[12]:
            symbols['red']['tar'].square = cursquare
            cursquare.symbol = symbols['red']['tar']
        if data[13]:
            symbols['red']['tri'].square = cursquare
            cursquare.symbol = symbols['red']['tri']
        if data[14]:
            symbols['blue']['bio'].square = cursquare
            cursquare.symbol = symbols['blue']['bio']
        if data[15]:
            symbols['blue']['hex'].square = cursquare
            cursquare.symbol = symbols['blue']['hex']
        if data[16]:
            symbols['blue']['tar'].square = cursquare
            cursquare.symbol = symbols['blue']['tar']
        if data[17]:
            symbols['blue']['tri'].square = cursquare
            cursquare.symbol = symbols['blue']['tri']
        if data[18]:
            symbols['green']['bio'].square = cursquare
            cursquare.symbol = symbols['green']['bio']
        if data[19]:
            symbols['green']['hex'].square = cursquare
            cursquare.symbol = symbols['green']['hex']
        if data[20]:
            symbols['green']['tar'].square = cursquare
            cursquare.symbol = symbols['green']['tar']
        if data[21]:
            symbols['green']['tri'].square = cursquare
            cursquare.symbol = symbols['green']['tri']
        if data[22]:
            symbols['yellow']['bio'].square = cursquare
            cursquare.symbol = symbols['yellow']['bio']
        if data[23]:
            symbols['yellow']['hex'].square = cursquare
            cursquare.symbol = symbols['yellow']['hex']
        if data[24]:
            symbols['yellow']['tar'].square = cursquare
            cursquare.symbol = symbols['yellow']['tar']
        if data[25]:
            symbols['yellow']['tri'].square = cursquare
            cursquare.symbol = symbols['yellow']['tri']

        line = file.readline ()

    return grid

def savemap ():
    file = open ("./first.map", 'w')

    string = ""
    for row in grid:
        for square in row:
            string += str (square.coords)
            if square.left:
                string += " 0"
            else:
                string += " 1"
            if square.right:
                string += " 0"
            else:
                string += " 1"
            if square.up:
                string += " 0"
            else:
                string += " 1"
            if square.down:
                string += " 0"
            else:
                string += " 1"
            if square.robot and square.robot.color == "red":
                string += " 1"
            else:
                string += " 0"
            if square.robot and square.robot.color == "blue":
                string += " 1"
            else:
                string += " 0"
            if square.robot and square.robot.color == "green":
                string += " 1"
            else:
                string += " 0"
            if square.robot and square.robot.color == "yellow":
                string += " 1"
            else:
                string += " 0"

            for color in symbols:
                for form in symbols[color]:
                    if symbols[color][form].square == square:
                        string += " 1"
                    else:
                        string += " 0"

            string += "\n"

    file.write (string)
    file.close ()

pygame.init ()

screen = pygame.display.set_mode ((640, 640))
pygame.display.set_caption ('Ricochet Robots')

squareimg = pygame.image.load ("./square.png")

red = Robot (pygame.image.load ("./redbot.png"), "red")
blue = Robot (pygame.image.load ("./bluebot.png"), "blue")
green = Robot (pygame.image.load ("./greenbot.png"), "green")
yellow = Robot (pygame.image.load ("./yellowbot.png"), "yellow")

symbols = {'red': {}, 'blue': {}, 'green': {}, 'yellow': {}}

for color in symbols:
    symbols[color]['bio'] = Symbol (pygame.image.load
                                    ("./" + color + "bio.png"), color)
    symbols[color]['hex'] = Symbol (pygame.image.load
                                    ("./" + color + "hex.png"), color)
    symbols[color]['tar'] = Symbol (pygame.image.load
                                    ("./" + color + "tar.png"), color)
    symbols[color]['tri'] = Symbol (pygame.image.load
                                    ("./" + color + "tri.png"), color)

grid = gengrid ()

mousepos = pygame.mouse.get_pos ()

selected = None

state = 0

while True:
    for event in pygame.event.get ():
        if event.type == QUIT:
            sys.exit ()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit ()
            elif event.key == K_DELETE:
                if selected and state == 0:
                    try:
                        left = grid[selected.coords[0]-1][selected.coords[1]]
                    except:
                        left = None
                    try:
                        right = grid[selected.coords[0]+1][selected.coords[1]]
                    except:
                        right = None
                    try:
                        up = grid[selected.coords[0]][selected.coords[1]-1]
                    except:
                        up = None
                    try:
                        down = grid[selected.coords[0]][selected.coords[1]+1]
                    except:
                        down = None

                    if left:
                        selected.left = left
                        selected.left.right = selected
                    if right:
                        selected.right = right
                        selected.right.left = selected
                    if up:
                        selected.up = up
                        selected.up.down = selected
                    if down:
                        selected.down = down
                        selected.down.up = selected
                elif state == 1:
                    if selected and selected.robot:
                        selected.robot.square = None
                        selected.robot = None
            elif event.key == K_LEFT:
                if selected and selected.left:
                    selected = selected.left
            elif event.key == K_RIGHT:
                if selected and selected.right:
                    selected = selected.right
            elif event.key == K_UP:
                if selected and selected.up:
                    selected = selected.up
            elif event.key == K_DOWN:
                if selected and selected.down:
                    selected = selected.down
            elif event.unicode == 's':
                state += 1
                if state == 6:
                    savemap ()
                    sys.exit ()
                print "newstate: ", state
            elif event.unicode == 'k':
                if state == 0 and selected and selected.up:
                    selected.up.down = None
                    selected.up = None
            elif event.unicode == 'j':
                if state == 0 and selected and selected.down:
                    selected.down.up = None
                    selected.down = None
            elif event.unicode == 'h':
                if state == 0 and selected and selected.left:
                    selected.left.right = None
                    selected.left = None

                symstate = 0
                if state == 2:
                    color = 'red'
                    symstate = 1
                elif state == 3:
                    color = 'blue'
                    symstate = 1
                elif state == 4:
                    color = 'green'
                    symstate = 1
                elif state == 5:
                    color = 'yellow'
                    symstate = 1

                if symstate and selected:
                    if symbols[color]['hex'].square:
                        symbols[color]['hex'].square.symbol = None
                    if not selected.symbol:
                        selected.symbol = symbols[color]['hex']
                        symbols[color]['hex'].square = selected
            elif event.unicode == 'l':
                if state == 0 and selected and selected.right:
                    selected.right.left = None
                    selected.right = None
            elif event.unicode == 'r':
                if state == 1 and selected:
                    if red.square:
                        red.square.robot = None
                    if not selected.robot:
                        selected.robot = red
                        red.square = selected
            elif event.unicode == 'g':
                if state == 1 and selected:
                    if green.square:
                        green.square.robot = None
                    if not selected.robot:
                        selected.robot = green
                        green.square = selected
                symstate = 0
                if state == 2:
                    color = 'red'
                    symstate = 1
                elif state == 3:
                    color = 'blue'
                    symstate = 1
                elif state == 4:
                    color = 'green'
                    symstate = 1
                elif state == 5:
                    color = 'yellow'
                    symstate = 1

                if symstate and selected:
                    if symbols[color]['tar'].square:
                        symbols[color]['tar'].square.symbol = None
                    if not selected.symbol:
                        selected.symbol = symbols[color]['tar']
                        symbols[color]['tar'].square = selected
            elif event.unicode == 'b':
                if state == 1 and selected:
                    if blue.square:
                        blue.square.robot = None
                    if not selected.robot:
                        selected.robot = blue
                        blue.square = selected
                symstate = 0
                if state == 2:
                    color = 'red'
                    symstate = 1
                elif state == 3:
                    color = 'blue'
                    symstate = 1
                elif state == 4:
                    color = 'green'
                    symstate = 1
                elif state == 5:
                    color = 'yellow'
                    symstate = 1
                    
                if symstate and selected:
                    if symbols[color]['bio'].square:
                        symbols[color]['bio'].square.symbol = None
                    if not selected.symbol:
                        selected.symbol = symbols[color]['bio']
                        symbols[color]['bio'].square = selected
            elif event.unicode == 'y':
                if state == 1 and selected:
                    if yellow.square:
                        yellow.square.robot = None
                    if not selected.robot:
                        selected.robot = yellow
                        yellow.square = selected
            elif event.unicode == 't':
                symstate = 0
                if state == 2:
                    color = 'red'
                    symstate = 1
                elif state == 3:
                    color = 'blue'
                    symstate = 1
                elif state == 4:
                    color = 'green'
                    symstate = 1
                elif state == 5:
                    color = 'yellow'
                    symstate = 1

                if symstate and selected:
                    if symbols[color]['tri'].square:
                        symbols[color]['tri'].square.symbol = None
                    if not selected.symbol:
                        selected.symbol = symbols[color]['tri']
                        symbols[color]['tri'].square = selected
        elif event.type == MOUSEMOTION:
            mousepos = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            for row in grid:
                for square in row:
                    if square.box.collidepoint (mousepos):
                        selected = square

    draw ()
    pygame.display.flip ()

    pygame.time.wait (100)
