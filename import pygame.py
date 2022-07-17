#!C:/Users/David/chess/bin/python
import pygame
import time
import sys

board = [[' ' for i in range(8)] for i in range(8)]

#Chess piece class which defines type of piece, what side its on, and if
#it has captured yet

class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.image = image
        self.killable = killable

#Creates instances of chess pieces
#Pawn
bp = Piece('b', 'p', 'b_pawn.png')
wp = Piece('w', 'p','w_pawn.png')
#king
bk = Piece('b', 'k', 'b_king.png')
wk = Piece('w', 'k', 'w_king.png')
#rook
br = Piece('b','r', 'b_rook.png')
wr = Piece('w','r', 'w_rook.png')
#bishop
bb = Piece('b','b', 'b_bishop.png')
wb = Piece('w','b', 'w_bishop.png')
#queen
bq = Piece('b','q', 'b_queen.png')
wq = Piece('w','q', 'w_queen.png')
#knight
bkn = Piece('b','kn', 'b_knight.png')
wkn = Piece('w','kn', 'w_knight.png')
#sets the starting order
start_order = (0,0) : pygame.image.load(br.image), 