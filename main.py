import pygame
import random
pygame.init()

class Board:
    PLAYER_HOVER_COLORS = [0, (255, 245, 161), (255, 166, 166)]

    def __init__(self, rows, cols, win):
        self.rows = rows
        self.cols = cols
        self.win = win
        self.width = 700
        self.height = 600
        self.tiles = [[Tile(0, i, j) for i in range(7)] for j in range(6)]
        self.turn = random.randint(1, 2)


    def place(self, pos):
        col = pos[0] // 100
        row = self.find_empty(col)
        if row == -1:
            return False
        else:
            self.tiles[row][col].value = self.turn

            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1

        if finished(self):
            return True

    def find_empty(self, col):
        # returns -1 if column is full, otherwise returns the row index of the last empty tile
        for i, row in enumerate(self.tiles):
            if i == 0 and row[col].value != 0:
                return -1
            elif row[col].value != 0:
                return (i-1)
            elif i == len(self.tiles) - 1 and row[col].value == 0:
                return i
            

    def draw(self, pos):    
        pygame.draw.rect(self.win, "BLUE", (0, 100, self.cols*100, self.rows*100))

        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].draw(self.win)

        pygame.draw.circle(self.win, self.PLAYER_HOVER_COLORS[self.turn], (pos[0] // 100 * 100 + 50, 50), 30, 0)
        pygame.draw.circle(self.win, self.PLAYER_HOVER_COLORS[self.turn], (pos[0] // 100 * 100 + 50, (self.find_empty(pos[0] // 100)) * 100 + 150 ), 30, 0)


class Tile:
    PLAYER_COLORS = [(255, 255, 255), (255, 229, 0), (255, 0, 0)]
    
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col


    def draw(self, win):
        pygame.draw.circle(win, self.PLAYER_COLORS[self.value], (self.row * 100 + 50, self.col  * 100 + 150), 30, 0)


def finished(board):
    for r in range(0, board.rows - 3):
        # check if a \ line is completed
        for c in range(0, board.cols - 3):
            tile = board.tiles[r][c].value
            if tile != 0:
                if tile == board.tiles[r+1][c+1].value and tile == board.tiles[r+2][c+2].value and tile == board.tiles[r+3][c+3].value:
                    return True
                
        # check if a / line is completed
        for c in range(3, board.cols):
            tile = board.tiles[r][c].value
            if tile != 0:
                if tile == board.tiles[r+1][c-1].value and tile == board.tiles[r+2][c-2].value and tile == board.tiles[r+3][c-3].value:
                    return True

        # check if a | line is completed
        for c in range(board.cols):
            tile = board.tiles[r][c].value
            if tile != 0:
                if tile == board.tiles[r+1][c].value and tile == board.tiles[r+2][c].value and tile == board.tiles[r+3][c].value:
                    return True
                
    # check if a _ line is completed
    for r in range(board.rows):
        for c in range(board.cols - 3):
            tile = board.tiles[r][c].value
            if tile != 0:
                if tile == board.tiles[r][c+1].value and tile == board.tiles[r][c+2].value and tile == board.tiles[r][c+3].value:
                    return True


def draw_window(win, board, pos):
    win.fill((255,255,255))
    board.draw(pos)


def main():
    win = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Connect Four")
    board = Board(6, 7, win)
    run = True
    while run:
        pos = pygame.mouse.get_pos()
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.place(pos):
                    print("Player", board.turn, "won")
                    run = False

        draw_window(win, board, pos)
        pygame.display.update()

if __name__ == '__main__':
    main()
