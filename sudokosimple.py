def isok(grid, x, y, n):
    # row
    for i in range(0, 9):
        if grid[x][i] == n:
            return 0
    # col
    for i in range(0, 9):
        if grid[i][y] == n:
            return 0

    # block
    boxx = x // 3
    boxy = y // 3
    for i in range(boxx * 3, boxx * 3 + 3):
        for j in range(boxy * 3, boxy * 3 + 3):
            if grid[i][j] == n:
                return 0

    return 1


def find_next(grid):
    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] == 0:
                return i, j

    return None


def solvesimple(grid):
    found = find_next(grid)
    if found is None:
        return 1
    else:
        x, y = found
        for i in range(1, 10):
            if isok(grid, x, y, i):
                grid[x][y] = i
                if solvesimple(grid):
                    return 1
                grid[x][y] = 0

    return 0


def givesolved(grid):
    if solvesimple(grid):
        return grid
    else:
        return None