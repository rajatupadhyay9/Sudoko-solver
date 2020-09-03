import pygame
import copy
from sudokosimple import givesolved
import getnewboard
import time


pygame.init()


# global variables and activity
difflevel = 0
while difflevel < 1 or difflevel > 3:
    difflevel = int(input("Enter difficulty level (1 to 3) : "))
board = getnewboard.createboard(str(difflevel))
solvedboard = copy.deepcopy(board)
if solvedboard is None:
    print("There was some issue with API please try again, Sorry")
    exit(0)
tempboard = copy.deepcopy(board)
opacity = [[0.5 if ele == 0 else 1 for ele in row] for row in board]
print(opacity)
solvedboard = givesolved(solvedboard)
boardr = 9
boardc = 9
mheight = 450
mwidth = 450
cubeh = 50
cubew = 50
selectedxy = None
font = pygame.font.SysFont("Ubuntu", 30)
mainsurface = pygame.display.set_mode((mheight, mwidth+40))
pygame.display.set_caption("Jatt Da Muqabla")


def createlayout():
    mainsurface.fill((0, 0, 0))
    for r in [0 * mheight / 3, 1 * mheight / 3, 2 * mheight / 3]:
        for c in [0 * mwidth / 3, 1 * mwidth / 3, 2 * mwidth / 3]:
            for i in [r + (0 * cubeh), r + (1 * cubeh), r + (2 * cubeh)]:
                for j in [c + (0 * cubew), c + (1 * cubew), c + (2 * cubew)]:
                    pygame.draw.rect(mainsurface, (40*j/75, 0, 40*i/75), (i, j, cubeh, cubew), 3)

    pygame.draw.line(mainsurface, (255, 255, 255), (0, 150), (450, 150), 2)
    pygame.draw.line(mainsurface, (255, 255, 255), (0, 300), (450, 300), 2)
    pygame.draw.line(mainsurface, (255, 255, 255), (150, 0), (150, 450), 2)
    pygame.draw.line(mainsurface, (255, 255, 255), (300, 0), (300, 450), 2)
    return


def filllayout():
    for i in range(boardr):
        for j in range(boardc):
            text = font.render(str(tempboard[i][j]) if tempboard[i][j] != 0 else " ", 1, (255 * opacity[i][j], 255 * opacity[i][j], 255 * opacity[i][j]))
            mainsurface.blit(text, (j * cubeh +20, i*cubew + 15))

    return


createlayout()
filllayout()
pygame.display.update()


def findempty():
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == 0:
                return i, j

    return None


def isvalid(r, c, n):
    # row
    for i in range(0, 9):
        if board[r][i] == n:
            return 0
    # col
    for i in range(0, 9):
        if board[i][c] == n:
            return 0

    # block
    boxx = r // 3
    boxy = c // 3
    for i in range(boxx * 3, boxx * 3 + 3):
        for j in range(boxy * 3, boxy * 3 + 3):
            if board[i][j] == n:
                return 0

    return 1


def place(r, c, acc):
    colors = (255, 0, 0) if acc == 'r' else (0, 255, 0)
    pygame.draw.rect(mainsurface, (0, 0, 0), (c*50, r*50, 50, 50))
    pygame.draw.rect(mainsurface, colors, (c * 50, r * 50, 50, 50), 3)
    text = font.render(str(board[r][c]), 1, (255, 255, 255))
    mainsurface.blit(text, (c * cubeh + 20, r * cubew + 15))
    pygame.time.delay(10)
    pygame.display.update()


def solvegui():
    found = findempty()
    if found is None:
        return 1

    r, c = found
    for i in range(1, 10):
        if isvalid(r, c, i):
            board[r][c] = i
            place(r, c, 'g')
            if solvegui():
                return 1
            board[r][c] = 0
            place(r, c, 'r')

    return 0


def heighlite():
    createlayout()
    filllayout()
    pygame.draw.rect(mainsurface, (255, 0, 0), (selectedxy[1] * 50, selectedxy[0] * 50, 50, 50), 3)
    pygame.display.update()


startat = time.time()
while True:
    if findempty() is None:
        timetext = font.render("Congratulations you won", 1, (255, 255, 255))
        pygame.draw.rect(mainsurface, (0, 0, 0), (0, 460, 300, 40))
        mainsurface.blit(timetext, (30, 460))
        pygame.display.update()

    for event in pygame.event.get():    # to quit
        if event.type == pygame.QUIT:   # when user
            pygame.quit()
            quit()                      # closes program
        if event.type == pygame.MOUSEBUTTONDOWN:    # if user selects a cube
            x, y = pygame.mouse.get_pos()           # get pos relative to upper corner
            y, x = x//50, y//50                     # convert them to index(s) and swap them
            selectedxy = (x, y)
            heighlite()
        if event.type == pygame.KEYDOWN:    # if user inputs a number and a cube is selected
            if event.key == pygame.K_SPACE:
                solvegui()

            if event.key == pygame.K_DELETE:
                if opacity[selectedxy[0]][selectedxy[1]] == 0.5:
                    tempboard[selectedxy[0]][selectedxy[1]] = 0
                    createlayout()
                    filllayout()
                    heighlite()
                    pygame.display.update()

            key = -1
            if event.key in range(49, 58):
                key = event.key - 48
            if event.key in range(257, 266):
                key = event.key - 256
            if key != -1 and opacity[selectedxy[0]][selectedxy[1]] == 0.5:
                tempboard[selectedxy[0]][selectedxy[1]] = key
                heighlite()

            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                if tempboard[selectedxy[0]][selectedxy[1]] == solvedboard[selectedxy[0]][selectedxy[1]]:
                    board[selectedxy[0]][selectedxy[1]] = tempboard[selectedxy[0]][selectedxy[1]]
                    opacity[selectedxy[0]][selectedxy[1]] = 1
                    createlayout()
                    filllayout()
                    heighlite()
                    pygame.display.update()
                else:
                    tempboard[selectedxy[0]][selectedxy[1]] = 0
                    createlayout()
                    filllayout()
                    heighlite()
                    pygame.display.update()

    timetext = font.render("Time : " + str(round(time.time() - startat)), 1, (255, 255, 255))
    pygame.draw.rect(mainsurface, (0, 0, 0), (300, 450, 150, 50))
    mainsurface.blit(timetext, (300, 460))
    pygame.display.update()
