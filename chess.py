
#! C:\Users\David\chess\env\Scripts\python
from urllib.parse import non_hierarchical
import pygame
import sys
import os
board = [['  ' for i in range(8)] for i in range(8)]

#Chess piece class which defines type of piece, what side its on, and if
#it has captured yet
width = 800
nodeSize = (width/8, width / 8)
class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.image = image
        self.killable = killable
#TODO: Update pictures
#Creates instances of chess pieces
#Pawn
bp = Piece('b', 'p', 'bp.png')
wp = Piece('w', 'p','wp.png')
#king
bk = Piece('b', 'k', 'bk.png')
wk = Piece('w', 'k', 'wk.png')
#rook
br = Piece('b','r', 'br.png')
wr = Piece('w','r', 'wr.png')
#bishop
bb = Piece('b','b', 'bb.png')
wb = Piece('w','b', 'wb.png')
#queen
bq = Piece('b','q', 'bq.png')
wq = Piece('w','q', 'wq.png')
#knight
bkn = Piece('b','kn', 'bkn.png')
wkn = Piece('w','kn', 'wkn.png')
#sets the starting order
pieces = [br, bkn, bp, wp, bk, wk, bb, bq, wq, wb, wkn, wr]
start = {}
#TODO: revise for efficency
#TODO: choose better piece images

def upload(pic):
    return os.path.join('chess-pieces', pic)
for x in range(0, 8):
    for y in range(2, 6):
        start[(x, y)] = None
for i in pieces:
    #black side
    if i.team == 'b':
        if(i.type == 'p' ):
            for n in range(0,8):
                start[(n, 1)] = pygame.image.load(upload(bp.image))

        #postions rook
        elif i.type == 'r':
            start[(0,0)] = pygame.image.load(upload(br.image))
            start[(7,0)] = pygame.image.load(upload(br.image))

        #postions for bishop
        elif i.type == 'b':
            start[(2,0)] = pygame.image.load(upload(bb.image))
            start[(5,0)] = pygame.image.load(upload(br.image))

        #positions for knight
        elif i.type == 'kn':
            start[(1,0)] = pygame.image.load(upload(bkn.image))
            start[(6,0)] = pygame.image.load(upload(bkn.image))
        #queen position
        elif i.type == 'q':
            start[(4,0)] = pygame.image.load(upload(bq.image))
        #king position
        else:
            start[(3,0)] = pygame.image.load(upload(bk.image))
    #white side
    elif i.team == 'w':
        #pawn positions 
        if i.type == 'p':
            for n in range(0,8):
                start[(n, 6)] = pygame.image.load(upload(wp.image))
        #bishop positions
        elif i.type == 'b':
            start[(2, 7)] = pygame.image.load(upload(wb.image))
            start[(5,7)] = pygame.image.load(upload(wb.image))
        #rook positions
        elif i.type == 'r':
            start[(0,7)] = pygame.image.load(upload(wr.image))
            start[(7,7)] = pygame.image.load(upload(wr.image))
        #positions for knight
        elif i.type == 'kn':
            start[(1,7)] = pygame.image.load(upload(wkn.image))
            start[(4,7)] = pygame.image.load(upload(wkn.image))
        #queen position
        elif i.type == 'q':
            start[(6,7)] = pygame.image.load(upload(wq.image))
        #king position
        else:
            start[(3,7)] = pygame.image.load(upload(wk.image))
for a in range(0, 8):
    for b in range(0, 8):
        if start[(a, b)] != None:
            start[(a, b)] = pygame.transform.scale(start[(a, b)], (nodeSize))
#creates board
def createBoard(board):
    board[0] = [br, bkn, bb, bq, bk, bb, bkn, br]
    board[7] = [br, bkn, bb, bk, bq, bb, bkn, br]
    for i in range(8):
        board[1][i] = bp
        board[6][i] = wp
    return board

def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True
#makes the boad readable
def convertBoard(board):
    output = ''
    for i in board:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output
#resets "x's" and capurted pieces
def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass
    return convertBoard(board)
#gives valid move using the board as the argument
def highlight(board):
    highlighted = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x ':
                highlighted.append((i, j))
            else:
                try: 
                    if board[i][j].killable:
                        highlighted.append((i, j))
                except:
                    pass
    return highlighted

def check_team(moves, index):
    row, col = index
    if moves % 2 == 0:
        if board[row][col].team == 'w':
            return True
    else:
        if board[row][col].team == 'b':
            return True
#determines moves based on the piece
#FIXME - When you select a piece it returns "Can't select" (1/2)
def select_moves(piece, index, moves):
    pt = piece.type
    if check_team(moves, index):
        if pt == 'p':
            if piece.team == 'b':
                return highlight(bPawnMv(index))
            else:
                return highlight(wPawnMv(index))
        elif pt == 'r':
            return highlight(rookMv(index))
        elif pt == 'b':
            return highlight(bishopMv(index))
        elif pt =='k':
            return highlight(kingMv(index))
        elif pt == 'q':
            return highlight(queenMv(index))
        else:
            return highlight(knightMv(index))
#defines how pawns move
def bPawnMv(index):
    if index[0] == 1:
        if board[index[0] + 2][index[1]] == '  ' and board[index[0] + 1][index[1]] == '  ':
            board[index[0]+ 2][index[1]] = 'x '
    bottom3 = [[index[0] + 1, index[1] + i] for i in range(-1, 2)]
    for positions in bottom3:
        if on_board(positions):
            if bottom3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'b':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else: 
                if board[positions[0]][positions[1]].team == '  ':
                    board[positions[0]][positions[1]] = 'x '
    return board

def wPawnMv(index):
    if index[0] == 6:
        if board[index[0] - 2][index[1]] == '  ' and board[index[0] - 1][index[1]] == '  ':
            board[index[0]- 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]
    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'w':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else: 
                if board[positions[0]][positions[1]].team == '  ':
                    board[positions[0]][positions[1]] = 'x '
    return board

def kingMv(index):
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 +x] == '  ':
                    board[index[0] - 1 +y][index[1] - 1 + x] == 'x '
                elif board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                    board[index[0] - 1 + y][index[1] - 1 + x].killable = True
    return board

def rookMv(index):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 -index[0])], 
                [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
                [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
                [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]
    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][board[positions[1]]] = 'x '

                elif board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                    board[positions[0]][positions[1]].killable = True
                    break
    return board

def bishopMv(index):
    diagonals = [[[index[0] + i, index[1] + i ] for i in range(1,8)], 
                 [[index[0] + i, index[1] - i] for i in range(1, 8)], 
                 [[index[0] - i, index[1] + i] for i in range(1,8)], 
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]
    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                elif board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                    board[positions[0]][positions[1]].killable = True
                    break
    return board

def queenMv(index):
    board = rookMv(index)
    board = bishopMv(index)
    return board
def knightMv(index):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board(index[0] + i, index[1] + j):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board [index[0] + i][index[1] + j] = 'x '
                    elif board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                        board[index[0] + i][index[1] + j].killable = True
    return board


win = pygame.display.set_mode((width, width))

pygame.display.set_caption("Chess")
white = (255, 255, 255)
grey = (128, 128, 128)
yellow = (204, 204, 0)
blue = (50, 255, 255)
black = (0, 0, 0)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.color = white
        self.occupied = None 

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, width / 8, width / 8))

    def setup(self, win):
        if start[(self.row, self.col)]:
            if start[(self.row, self.col)] == None:
                pass
            else:
                win.blit(start[(self.row, self.col)], (self.x, self.y))
def make_grid(rows, width):
    grid = []
    gap = width//rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i + j)%2 == 1:
                grid[i][j].color = grey
    return grid
def drawGrid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, black, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, black, (j * gap, 0), (j * gap, width))

def updateDisplay(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    drawGrid(win, rows, width)
    pygame.display.update()

def findNode(pos, width):
    interval = width / 8
    y, x = pos 
    rows = y // interval
    columns = x  // interval
    return int(rows), int(columns)
def potentialMv(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].color = blue

def move(originalPos, finalPosition, win):
    start[finalPosition] = start[originalPos]
    start[originalPos] = None

def removeHightlight(grid):
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].color = white
            else:
                grid[i][j].color = grey
    return grid
createBoard(board )
#FIXME - When you select a piece it returns "Can't select" (2/2)
def main(win, width):
    moves = 0
    selected = False
    pieceToMove = []
    grid = make_grid(8, width)
    while True:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #BUG - Part of the piece select issue
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = findNode(pos, width)
                if selected == False:
                    try:
                        possible = select_moves((board[y][x]), (x, y), moves)
                        for positions in possible:
                            row, col = positions
                            grid[row][col].color = blue
                        pieceToMove = x, y
                        selected = True
                    except:
                        pieceToMove = []
                        print('Can\'t select')
                else:
                    try:
                        if board[x][y].killable == True:
                            row, col = pieceToMove
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            removeHightlight(grid)
                            move((col, row), (y, x), win)
                            moves += 1
                            print(convertBoard(board))
                        else:
                            deselect()
                            removeHightlight(grid)
                            selected = False
                            print("Deselected")
                    except:
                        if board[x][y] == 'x ':
                            row, col = pieceToMove
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            removeHightlight(grid)
                            move((col, row), (y, x), win)
                            moves += 1 
                            print(convertBoard(board)) 
                        else:
                            deselect()
                            removeHightlight(grid)
                            selected = False
                            print("Invalid Move")
                    selected = False
            updateDisplay(win, grid, 8, width)

main(win, width)

