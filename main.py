import pygame
import numpy as np
import time


# constants
WIDTH, HEIGHT = 700, 700
WHITE_CELL = (255, 255, 255)
BG = (25, 25, 25)

# main window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# title
pygame.display.set_caption("Life Game")

# number of cells
nxC, nyC = 50, 50
# dimensions
dimCW = WIDTH / nxC
dimCH = HEIGHT / nyC
# cell's state. Alive = 1; Dead = 0;
gameState = np.zeros((nxC, nyC))


run = True
pauseRun = False
# FPS = 60
clock = pygame.time.Clock()
while run:
    # clock.tick(FPS)

    newGameState = np.copy(gameState)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            pauseRun = not pauseRun

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            #newStatus[x,y] = np.abs(newStatus[x,y]-1)
            newGameState[x, y] = not mouseClick[2]

    # clean background
    WIN.fill(BG)

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseRun:

                # number of neighbors: Toroidal form
                n_neight = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                    gameState[(x) % nxC, (y - 1) % nyC] + \
                    gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                    gameState[(x - 1) % nxC, (y) % nyC] + \
                    gameState[(x + 1) % nxC, (y) % nyC] + \
                    gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                    gameState[(x) % nxC, (y + 1) % nyC] + \
                    gameState[(x + 1) % nxC, (y + 1) % nyC]

                # ! Not working
                # number of neighbors: Regular form
                # n_neight = gameState[(x - 1), (y - 1)] + \
                #     gameState[(x), (y - 1)] + \
                #     gameState[(x + 1), (y - 1)] + \
                #     gameState[(x - 1), (y)] + \
                #     gameState[(x + 1), (y)] + \
                #     gameState[(x - 1), (y + 1)] + \
                #     gameState[(x), (y + 1)] + \
                #     gameState[(x + 1), (y + 1)]

                # Rule #1 : a dead cell with 3 living neighbors will revive
                if gameState[x, y] == 0 and n_neight == 3:
                    newGameState[x, y] = 1
                # Rule #2 : a living cell with less than 2 or more than 3 living neighbors will die
                elif gameState[x, y] == 1 and (n_neight < 2 or n_neight > 3):
                    newGameState[x, y] = 0

            poly = [(x * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    (x * dimCW, (y+1) * dimCH)]
            # drawing each cells depending the states
            if newGameState[x, y] == 0:
                pygame.draw.polygon(WIN, (47, 40, 34), poly, 1)
            else:
                pygame.draw.polygon(WIN, (WHITE_CELL), poly, 0)
                pygame.draw.polygon(WIN, (47, 40, 34), poly, 1)

    # Refresh
    gameState = np.copy(newGameState)
    # time.sleep(0.1)
    pygame.display.update()

# quit
pygame.quit()
