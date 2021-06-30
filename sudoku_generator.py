import random


def generate_sudoku(num_givens):
    grid = [[0] * 9 for i in range(9)]
    __generate_sudoku_helper(grid)

    num_removals = 81 - num_givens

    locations_to_remove = set()

    while len(locations_to_remove) < num_removals:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        locations_to_remove.add((x, y))

    for location in locations_to_remove:
        grid[location[0]][location[1]] = 0

    return grid


def __generate_sudoku_helper(grid):
    """
    solves sodoku grid
    :param grid: the sudoku grid to be solved
    :return: whether or not the grid has been solved
    """
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(nums)

    grid_size = len(grid)
    for x in range(0, grid_size):
        for y in range(0, grid_size):
            # found empty spot
            if grid[x][y] == 0:
                for num in nums:
                    if __is_possible(x, y, num, grid):
                        grid[x][y] = num
                        # go to next empty spot
                        if __generate_sudoku_helper(grid):
                            # found solution
                            return True
                        # reach here when we fail, so backtrack
                        grid[x][y] = 0
                # return false when we tried all possible numbers for the empty spot but still doesn't work
                return False
    # no more free cells, grid is solved
    return True


def __is_possible(x, y, num, grid):
    """
    Check to see if a number is possible at a give location on the grid
    :param x: the row on the grid
    :param y: the column on the grid
    :param num: the number we want to try
    :param grid: the sudoku grid
    :return: boolean of whether or not it is possible to put that number at the x, y location
    """
    grid_size = len(grid)
    # check row
    for i in range(0, grid_size):
        if grid[x][i] == num:
            return False
    # check column
    for i in range(0, grid_size):
        if grid[i][y] == num:
            return False

    # check the square
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[x0 + i][y0 + j] == num:
                return False

    return True
