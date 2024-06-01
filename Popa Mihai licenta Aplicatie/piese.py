import pygame
import os

IMG_DIR = "img"
PIECE_SIZE = (55, 55)
RECT = (113, 113, 525, 525)
STARTX = RECT[0]
STARTY = RECT[1]
RECT_WIDTH = RECT[2] / 8
RECT_HEIGHT = RECT[3] / 8

def load_image(file):
    return pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, file)), PIECE_SIZE)

b_pieces = ["black bishop.png", "black king.png", "black knight.png", "black pawn.png", "black queen.png", "black rook.png"]
w_pieces = ["white bishop.png", "white king.png", "white knight.png", "white pawn.png", "white queen.png", "white rook.png"]

B = [load_image(file) for file in b_pieces]
W = [load_image(file) for file in w_pieces]

class Piece:
    img = -1

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False
        self.moved = False  

    def isSelected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def draw(self, win, color):
        drawThis = W[self.img] if self.color == "w" else B[self.img]
        x = round(STARTX + (self.col * RECT_WIDTH))
        y = round(STARTY + (self.row * RECT_HEIGHT))

        if self.selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)

        win.blit(drawThis, (x, y))

    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def __str__(self):
        return f"{self.col} {self.row}"

class Bishop(Piece):
    img = 0

    def valid_moves(self, board):
        moves = []
        directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]

        for direction in directions:
            x, y = direction
            chain = 1
            while True:
                new_row = self.row + chain * x
                new_col = self.col + chain * y
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    p = board[new_row][new_col]
                    if p == 0:
                        moves.append((new_col, new_row))
                    elif p.color != self.color:
                        moves.append((new_col, new_row))
                        break
                    else:
                        break
                else:
                    break
                chain += 1
        return moves

class King(Piece):
    img = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True

    def valid_moves(self, board):
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1), 
            (1, -1), (1, 0), (1, 1), 
            (0, -1), (0, 1)
        ]

        for d in directions:
            new_row, new_col = self.row + d[0], self.col + d[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                p = board[new_row][new_col]
                if p == 0 or p.color != self.color:
                    moves.append((new_col, new_row))
        return moves

class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        moves = []
        directions = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2), 
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for d in directions:
            new_row, new_col = self.row + d[0], self.col + d[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                p = board[new_row][new_col]
                if p == 0 or p.color != self.color:
                    moves.append((new_col, new_row))
        return moves

class Pawn(Piece):
    img = 3

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.queen = False
        self.pawn = True

    def valid_moves(self, board):
        moves = []
        direction = 1 if self.color == "b" else -1
        start_row = 1 if self.color == "b" else 6
        end_row = 6 if self.color == "b" else 1

        if 0 <= self.row + direction < 8:
            if board[self.row + direction][self.col] == 0:
                moves.append((self.col, self.row + direction))
                if self.row == start_row and board[self.row + 2 * direction][self.col] == 0:
                    moves.append((self.col, self.row + 2 * direction))

        for dc in [-1, 1]:
            if 0 <= self.col + dc < 8 and 0 <= self.row + direction < 8:
                p = board[self.row + direction][self.col + dc]
                if p != 0 and p.color != self.color:
                    moves.append((self.col + dc, self.row + direction))

        return moves

class Queen(Piece):
    img = 4

    def valid_moves(self, board):
        moves = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), 
            (-1, 1), (-1, -1), (1, 1), (1, -1)
        ]

        for d in directions:
            for chain in range(1, 8):
                new_row = self.row + d[0] * chain
                new_col = self.col + d[1] * chain
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    p = board[new_row][new_col]
                    if p == 0:
                        moves.append((new_col, new_row))
                    elif p.color != self.color:
                        moves.append((new_col, new_row))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Rook(Piece):
    img = 5

    def valid_moves(self, board):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d in directions:
            for chain in range(1, 8):
                new_row = self.row + d[0] * chain
                new_col = self.col + d[1] * chain
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    p = board[new_row][new_col]
                    if p == 0:
                        moves.append((new_col, new_row))
                    elif p.color != self.color:
                        moves.append((new_col, new_row))
                        break
                    else:
                        break
                else:
                    break
        return moves
