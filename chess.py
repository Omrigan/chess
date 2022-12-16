#!/usr/bin/env python3
#
from copy import deepcopy

class Piece:
    def __init__(self, name, white):
        self.name = name
        self.white = white


def move_king(old, new):
    return abs(old[0] - new[0]) <= 1 and abs(old[1] - new[1]) <= 1

def move_rook(old, new):
    return old[0] == new[0] or old[1] == new[1]

def move_bishop(old, new):
    return abs(old[0] - new[0]) == abs(old[1] - new[1])

def move_queen( old, new):
    return move_bishop(old, new) or move_rook(old, new)

def move_knight(old, new):
    return abs(old[0] - new[0]) * abs(old[1] - new[1]) == 2

def walk_white_pawn(old, new):
    if old[0] == 1 and new[0] == 3:
        return True
    return old[0] + 1 == new[0]

def walk_black_pawn(old, new):
    if old[0] == 6 and new[0] == 4:
        return True
    return old[0] - 1 == new[0]

def take_white_pawn(board, old, new):
    return old[0] + 1 == new[0]

def take_black_pawn(board, old, new):
    return old[0] - 1 == new[0]


def apply_move(board, old, new):
    new_board = deepcopy(board)
    new_board[new[0]][new[1]] = new_board[old[0]][old[1]]
    new_board[old[0]][old[1]] = None
    if new_board[new[0]][new[1]].name == 'pawn' and new[0] in (0, 7):
        new_board[new[0]][new[1]].name = 'queen'
    return new_board

def parse(sq):
    return (int(sq[1]) - 1, ord(sq[0]) - ord('a'))

class State:
    def __init__(self, board, white):
        self.board = board
        self.white = white

    def init(self):
        self.board = [[None for i in range(8)] for j in range(8)]
        self.board[0] = [
            Piece('rook', True), Piece('knight', True), Piece('bishop', True),
            Piece('queen', True), Piece('king', True), Piece('bishop', True),
            Piece('knight', True), Piece('rook', True)]
        self.board[1] = [Piece('pawn', True) for i in range(8)]
        self.board[6] = [Piece('pawn', False) for i in range(8)]
        self.board[7] = [
            Piece('rook', False), Piece('knight', False), Piece('bishop', False),
            Piece('queen', False), Piece('king', False), Piece('bishop', False),
            Piece('knight', False), Piece('rook', False)]
        self.white = True


    def walk_pawn(self, old, new):
        if self.white:
            return walk_white_pawn(old, new)
        return walk_black_pawn(old, new)

    def take_pawn(self, old, new):
        if self.white:
            return take_white_pawn(old, new)
        return take_black_pawn(old, new)

    def move_pawn(self, old, new):
        if self.board[new[0]][new[1]] is None:
            return old[1] == new[1] and self.walk_pawn(old, new)
        return abs(old[1] - new[1]) == 1 and self.take_pawn(old, new)


    def can_move_piece(self, old, new):
        piece = self.board[old[0]][old[1]]
        if old == new:
            return False
        if piece is None:
            return False
        if piece.white != self.white:
            return False
        if self.board[new[0]][new[1]] is not None and \
            self.board[new[0]][new[1]].white == self.white:
            return False
        if piece.name == 'king':
            return move_king(old, new)
        if piece.name == 'rook':
            return move_rook(old, new)
        if piece.name == 'bishop':
            return move_bishop(old, new)
        if piece.name == 'queen':
            return move_queen(old, new)
        if piece.name == 'knight':
            return move_knight(old, new)
        if piece.name == 'pawn':
            return self.move_pawn(old, new)
        return False

    def is_check(self):
        king = None
        board = self.board
        white = self.white
        for i in range(8):
            for j in range(8):
                if board[i][j] is not None and \
                    board[i][j].name == 'king' and board[i][j].white == white:
                    king = (i, j)
        for i in range(8):
            for j in range(8):
                if board[i][j] is not None and board[i][j].white != white and \
                    self.can_move_piece((i, j), king):
                    return True
        return False

    def can_move_no_check(self, old, new):
        if self.can_move_piece(old, new):
            return not State(apply_move(self.board, old, new),
                             not self.white).is_check()

    def do_move(self, old, new):
        if self.can_move_no_check(old, new):
            self.board = apply_move(self.board, old, new)
            self.white = not self.white
            return True
        return False

    def print(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is None:
                    print('.', end='')
                else:
                    name = self.board[i][j].name
                    if name == "knight":
                        name = "n"
                    if self.board[i][j].white:
                        print(name[0].upper(), end='')
                    else:
                        print(name[0], end='')
            print()
        print()

    def move(self, old, new):
        return self.do_move(parse(old), parse(new))

    def can(self, old, new):
        return self.can_move_no_check(parse(old), parse(new))

board = State(None, True)
board.init()
board.print()
assert not board.can('e2', 'e2')
assert not board.can('e2', 'e5')
assert not board.can('e2', 'f4')
assert not board.can('e1', 'e2')
assert board.can('b1', 'c3')
assert board.can('e2', 'e4')


assert board.move('f2', 'f3')
board.print()
assert board.move('e7', 'e5')
board.print()
assert board.move('g2', 'g4')
board.print()
assert board.move('d8', 'h4')
board.print()
print("checkmate")
