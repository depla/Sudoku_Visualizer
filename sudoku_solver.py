import pygame
import sys
import copy


class Solver:

    def __init__(self, board):
        """
        Constructor is injected with the board so that the solver can update the screen with the solution with the
        board methods
        :param board:
        """
        self.board = board

    def __is_possible(self, x, y, num, grid):
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

        # check the smaller square grids
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if grid[x0 + i][y0 + j] == num:
                    return False

        return True

    @staticmethod
    def is_valid_grid(grid):
        """
        Checks to see if a sudoku grid is valid or not (doesn't break any of the constraints of sudoku)
        :param grid: The grid in question
        :return: Boolean of whether or not the grid is valid
        """
        # init data
        rows = [{} for i in range(9)]
        columns = [{} for i in range(9)]
        boxes = [{} for i in range(9)]

        # validate a board
        for i in range(9):
            for j in range(9):
                num = grid[i][j]
                if num != 0:
                    box_index = (i // 3) * 3 + j // 3

                    # keep the current cell value
                    rows[i][num] = rows[i].get(num, 0) + 1
                    columns[j][num] = columns[j].get(num, 0) + 1
                    boxes[box_index][num] = boxes[box_index].get(num, 0) + 1

                    # check if this value has been already seen before
                    if rows[i][num] > 1 or columns[j][num] > 1 or boxes[box_index][num] > 1:
                        return False
        return True

    def solve_sudoku_visualizer(self, grid):
        """
        Solves the sudoku puzzle and updates the screen to visualize the recursive backtracking algorithm
        :param grid: The sudoku grid to be solved
        :return: Whether or not the grid has been solved
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.board.grid = copy.deepcopy(self.board.original_grid)
                    return True

        grid_size = len(grid)
        for x in range(0, grid_size):
            for y in range(0, grid_size):
                # found empty spot
                if grid[x][y] == 0:
                    for num in range(1, 10):
                        if self.__is_possible(x, y, num, grid):
                            grid[x][y] = num
                            self.board.draw_background()
                            self.board.draw_numbers()
                            self.board.current_location = (x, y)
                            self.board.highlight_solution(self.board.current_location)
                            pygame.display.flip()
                            pygame.time.delay(50)
                            # go to next empty spot
                            if self.solve_sudoku_visualizer(grid):
                                # found solution
                                return True
                            # reach here when we fail, so backtrack
                            grid[x][y] = 0
                            self.board.draw_background()
                            self.board.draw_numbers()
                            self.board.current_location = (x, y)
                            self.board.highlight_solution(self.board.current_location)
                            pygame.display.flip()
                            pygame.time.delay(50)
                    # return false when we tried all possible numbers for the empty spot but still doesn't work
                    return False
        # no more free cells, grid is solved
        return True
