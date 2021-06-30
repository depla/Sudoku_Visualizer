import pygame
import sys
import copy
import sudoku_solver
import sudoku_generator


class Board:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku Visualizer")
        self.screen_size = 660
        self.margin = 15
        self.cell_size = (self.screen_size - 2 * self.margin) // 9
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size + 100))
        self.grid_font = pygame.font.SysFont("comicsans", 40)
        self.instruction_font = pygame.font.SysFont("arial", 20)
        self.grid = [[0] * 9 for i in range(9)]
        self.original_grid = [[0] * 9 for i in range(9)]

        self.current_location = (-1, -1)

    def draw_background(self):
        self.screen.fill(pygame.Color("white"))
        self.display_instructions()
        # draw board
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect(self.margin, self.margin,
                                                                         self.screen_size - 2 * self.margin,
                                                                         self.screen_size - 2 * self.margin), 5)
        for i in range(1, 9):
            if i % 3 == 0:
                line_width = 5
            else:
                line_width = 1

            # draw vertical lines
            pygame.draw.line(self.screen, pygame.Color("black"),
                             pygame.Vector2(i * self.cell_size + self.margin, self.margin),
                             pygame.Vector2(i * self.cell_size + self.margin, self.screen_size - self.margin),
                             line_width)
            # draw horizontal lines
            pygame.draw.line(self.screen, pygame.Color("black"),
                             pygame.Vector2(self.margin, i * self.cell_size + self.margin),
                             pygame.Vector2(self.screen_size - self.margin, i * self.cell_size + self.margin),
                             line_width)

    def draw_numbers(self):
        offset = self.cell_size // 2 + self.margin // 2

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                current_number = self.grid[i][j]
                if current_number is not 0:
                    text = self.grid_font.render(str(current_number), True, pygame.Color("black"))
                    self.screen.blit(text, pygame.Vector2(j * self.cell_size + offset,
                                                          i * self.cell_size + offset))

    def display_instructions(self):
        text = self.instruction_font.render("Click cells and edit with 1-9 (backspace clears a cell)",
                                            True, pygame.Color("black"))
        self.screen.blit(text, pygame.Vector2(self.margin, self.screen_size - 10))
        text = self.instruction_font.render("g = generate puzzle", True, pygame.Color("black"))
        self.screen.blit(text, pygame.Vector2(self.margin, self.screen_size + 10))
        text = self.instruction_font.render("space = solve puzzle / cancel solve", True, pygame.Color("black"))
        self.screen.blit(text, pygame.Vector2(self.margin, self.screen_size + 30))
        text = self.instruction_font.render("c = clear grid", True, pygame.Color("black"))
        self.screen.blit(text, pygame.Vector2(self.margin, self.screen_size + 50))
        text = self.instruction_font.render("r = remove solution", True, pygame.Color("black"))
        self.screen.blit(text, pygame.Vector2(self.margin, self.screen_size + 70))

    def get_selected_cell(self, pos):
        selected_cell = ((pos[1] - self.margin) // self.cell_size, (pos[0] - self.margin) // self.cell_size)
        if 0 <= selected_cell[0] <= 8 and 0 <= selected_cell[1] <= 8:
            return selected_cell
        else:
            return None

    def highlight_cell(self, cell):
        self.draw_background()
        self.draw_numbers()
        if 0 <= cell[0] <= 8 and 0 <= cell[1] <= 8:
            pygame.draw.rect(self.screen, pygame.Color("red"), pygame.Rect(self.margin + self.cell_size * cell[1],
                                                                           self.margin + self.cell_size * cell[0],
                                                                           self.cell_size, self.cell_size), 7)

    def highlight_solution(self, cell):
        self.draw_background()
        self.draw_numbers()
        offset = self.cell_size // 2 + self.margin // 2
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] is not 0 and self.original_grid[i][j] is 0:
                    current_number = self.grid[i][j]
                    text = self.grid_font.render(str(current_number), True, pygame.Color("green"))
                    self.screen.blit(text, pygame.Vector2(j * self.cell_size + offset,
                                                          i * self.cell_size + offset))
        if 0 <= cell[0] <= 8 and 0 <= cell[1] <= 8:
            pygame.draw.rect(self.screen, pygame.Color("blue"), pygame.Rect(self.margin + self.cell_size * cell[1],
                                                                            self.margin + self.cell_size * cell[0],
                                                                            self.cell_size, self.cell_size), 7)

    def update_grid(self, row, col, entered_number):
        self.grid[row][col] = entered_number
        self.original_grid[row][col] = entered_number
        self.draw_numbers()

    def clear_grid(self):
        self.grid = [[0] * 9 for i in range(9)]
        self.original_grid = [[0] * 9 for i in range(9)]
        self.draw_background()
        self.draw_numbers()
        self.current_location = (-1, -1)

    def remove_solution(self):
        self.grid = self.original_grid
        self.draw_background()
        self.draw_numbers()
        self.current_location = (-1, -1)


    def run_game(self):
        self.draw_background()
        self.draw_numbers()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    selected_cell = self.get_selected_cell(pos)
                    if selected_cell is not None:
                        # highlight the selected cell
                        self.highlight_cell(selected_cell)
                        self.current_location = (selected_cell[0], selected_cell[1])
                    else:
                        # redraw the board
                        self.draw_background()
                        self.draw_numbers()
                        self.current_location = (-1, -1)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if sudoku_solver.Solver.is_valid_grid(self.grid):
                            self.original_grid = copy.deepcopy(self.grid)
                            solver = sudoku_solver.Solver(self)
                            solver.solve_sudoku_visualizer(self.grid)
                            self.draw_background()
                            self.draw_numbers()
                            self.current_location = (-1, -1)
                            self.highlight_solution(self.current_location)
                    if event.key == pygame.K_c:
                        self.clear_grid()
                    if event.key == pygame.K_r:
                        self.remove_solution()
                    if event.key == pygame.K_g:
                        self.grid = sudoku_generator.generate_sudoku(30)
                        self.original_grid = self.grid
                        self.draw_background()
                        self.draw_numbers()

                if self.current_location[0] is not -1 and self.current_location[1] is not -1:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.update_grid(self.current_location[0], self.current_location[1], 1)
                        if event.key == pygame.K_2:
                            self.update_grid(self.current_location[0], self.current_location[1], 2)
                        if event.key == pygame.K_3:
                            self.update_grid(self.current_location[0], self.current_location[1], 3)
                        if event.key == pygame.K_4:
                            self.update_grid(self.current_location[0], self.current_location[1], 4)
                        if event.key == pygame.K_5:
                            self.update_grid(self.current_location[0], self.current_location[1], 5)
                        if event.key == pygame.K_6:
                            self.update_grid(self.current_location[0], self.current_location[1], 6)
                        if event.key == pygame.K_7:
                            self.update_grid(self.current_location[0], self.current_location[1], 7)
                        if event.key == pygame.K_8:
                            self.update_grid(self.current_location[0], self.current_location[1], 8)
                        if event.key == pygame.K_9:
                            self.update_grid(self.current_location[0], self.current_location[1], 9)
                        if event.key == pygame.K_BACKSPACE:
                            self.update_grid(self.current_location[0], self.current_location[1], 0)

                        self.highlight_cell(self.current_location)
                # Update the full display Surface to the screen
                pygame.display.flip()
