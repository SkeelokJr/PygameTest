import pygame
import math

#setup
pygame.init()
sWidth, sHeight = 1280, 720
screen = pygame.display.set_mode((sWidth, sHeight))
clock = pygame.time.Clock()
running = True

# create board
boardBorderColor, boardColor = pygame.Color(255, 255, 255), pygame.Color(145, 100, 80)
boardSize = 500
boardBorderWidth = 3
boardX, boardY = sWidth/2 - boardSize/2, sHeight/2 - boardSize/2
boardBorder = pygame.Rect(boardX, boardY, boardSize, boardSize)
boardMiddle = pygame.Rect(boardX+boardBorderWidth, boardY+boardBorderWidth, boardSize-2*boardBorderWidth, boardSize-2*boardBorderWidth)

#create squares [file(a=0,h=7)][rank(0-7)]
numSquares = 64
lightColor = pygame.Color(255,255,255)
darkColor = pygame.Color(31,31,127)
hoverColor = pygame.Color(127,127,127)
moveColor = pygame.Color(255,255,0)
boardGap = 50
Squares = []
for i in range(numSquares):
    file, rank = int(i / 8), i % 8
    squareColor = None
    if (file + rank) % 2 == 0:
        squareColor = darkColor
    else:
        squareColor = lightColor
    squareSize = round((boardSize - 2*boardGap) / 8)
    squareX = boardX + boardGap + (file*squareSize)
    squareY = (boardY+boardSize) - 2*boardGap - (rank*squareSize)
    squareRect = pygame.Rect(squareX, squareY, squareSize, squareSize)
    squareData = {
        "file": file,
        "rank": rank,
        "color": squareColor,
        "rect": squareRect,
        "highlight_color": []
    }
    Squares.append(squareData)

# create pieces
Pieces = []

# initialize dynamic variables
mouseX, mouseY = 0, 0
mouseFile, mouseRank = None, None

def drawBoard():
    pygame.draw.rect(screen, boardBorderColor, boardBorder)
    pygame.draw.rect(screen, boardColor, boardMiddle)

def drawSquares():
    for s in Squares:
        if s["highlight_color"]:
            pygame.draw.rect(screen, s["color"].lerp(s["highlight_color"][-1], 0.2), s["rect"])
        else:
            pygame.draw.rect(screen, s["color"], s["rect"])

def getPieceAt(file, rank):
    for piece in Pieces:
        if piece["file"] == file and piece["rank"] == rank:
            return piece
    return None

def getMoves(piece):
    moves = []
    file, rank = piece["file"], piece["rank"]
    color = piece["color"]
    match piece["type"]:
        case "pawn":
            if color == "white":
                if not getPieceAt(file, rank+1) and rank < 7: 
                    moves.append((file, rank+1))
                    if not piece["hasMoved"] and rank < 6 and not getPieceAt(file, rank+2):
                        moves.append((file, rank+2))
                if file > 0 and rank < 7:
                    other = getPieceAt(file-1, rank+1)
                    if other and other["color"] == "black":
                        moves.append((file-1,rank+1))
                if file < 7 and rank < 7:
                    other = getPieceAt(file+1, rank+1)
                    if other and other["color"] == "black":
                        moves.append((file+1,rank+1))
            else:
                if not getPieceAt(file, rank-1) and rank > 0: 
                    moves.append((file, rank-1))
                    if not piece["hasMoved"] and rank > 1 and not getPieceAt(file, rank-2):
                        moves.append((file, rank-2))
                if file > 0 and rank > 0:
                    other = getPieceAt(file-1, rank-1)
                    if other and other["color"] == "white":
                        moves.append((file-1,rank-1))
                if file < 7 and rank > 0:
                    other = getPieceAt(file+1, rank-1)
                    if other and other["color"] == "white":
                        moves.append((file+1,rank-1))
        case "knight":
            other = getPieceAt(file-2, rank+1)
            if file >= 2 and rank <= 6 and (not other or not other["color"] == color):
                moves.append((file-2, rank+1))
            other = getPieceAt(file-1, rank+2)
            if file >= 1 and rank <= 5 and (not other or not other["color"] == color):
                moves.append((file-1, rank+2))
            other = getPieceAt(file+2, rank+1)
            if file <= 5 and rank <= 6 and (not other or not other["color"] == color):
                moves.append((file+2, rank+1))
            other = getPieceAt(file+1, rank+2)
            if file <= 6 and rank <= 5 and (not other or not other["color"] == color):
                moves.append((file+1, rank+2))
            other = getPieceAt(file-2, rank-1)
            if file >= 2 and rank >= 1 and (not other or not other["color"] == color):
                moves.append((file-2, rank-1))
            other = getPieceAt(file-1, rank-2)
            if file >= 1 and rank >= 1 and (not other or not other["color"] == color):
                moves.append((file-1, rank-2))
            other = getPieceAt(file+2, rank-1)
            if file <= 5 and rank >= 1 and (not other or not other["color"] == color):
                moves.append((file+2, rank-1))
            other = getPieceAt(file+1, rank-2)
            if file <= 6 and rank >= 2 and (not other or not other["color"] == color):
                moves.append((file+1, rank-2))
        case "bishop":
            for d in range(1, min(8-file, 8-rank)): # top right diagonal
                other = getPieceAt(file+d, rank+d)
                if other:
                    if other["color"] == color:
                        break
                    else:
                        moves.append((file+d, rank+d))
                        break
                else:
                    moves.append((file+d, rank+d))
        case "rook":
            pass
        case "queen":
            pass
        case "king":
            pass
    return moves

def createPiece(color, type, file, rank):
    fil = ""
    if color == "white":
        fil += "w"
    else:
        fil += "b"
    match type:
        case "pawn":
            fil += "p"
        case "knight":
            fil += "n"
        case "bishop":
            fil += "b"
        case "rook":
            fil += "r"
        case "queen":
            fil += "q"
        case "king":
            fil += "k"
    filePath = "{}.png"
    pieceImage = pygame.image.load(filePath.format(fil))
    pieceRect = pieceImage.get_rect()
    pieceX = boardX + boardGap + (file*squareSize)
    pieceY = (boardY+boardSize) - 2*boardGap - (rank*squareSize)
    pieceRect.topleft = (pieceX, pieceY)
    pieceData = {
        "color": color,
        "type": type,
        "file": file,
        "rank": rank,
        "hasMoved": False,
        "image": pieceImage,
        "rect": pieceRect
    }
    Pieces.append(pieceData)



def drawPieces():
    for piece in Pieces:
        screen.blit(piece["image"], piece["rect"])

def coordsToFileRank(x, y):
    if x >= boardX+boardGap and x < boardX+boardSize-boardGap and y > boardY+boardGap and y <= boardY+boardSize-boardGap:
        file = int((x - boardX - boardGap) / squareSize)
        rank = int((boardY + boardSize - 2*boardGap - y) / squareSize + 1)
        return (file, rank)
    return (None, None)

def getMouseInfo():
    global mouseFile, mouseRank
    mousePos = pygame.mouse.get_pos()
    mouseX, mouseY = mousePos[0], mousePos[1]
    mouseLoc = coordsToFileRank(mouseX, mouseY)
    mouseFile, mouseRank = mouseLoc[0], mouseLoc[1]
    for piece in Pieces:
        if piece["file"] == mouseFile and piece["rank"] == mouseRank:
            moves = getMoves(piece)
            print(*moves)
            for move in moves:
                highlightSquare(*move, moveColor)

def highlightSquare(file, rank, color):
    for square in Squares:
        if square["file"] == file and square["rank"] == rank:
            square["highlight_color"].append(color)

def clearHighlights():
    for square in Squares:
        square["highlight_color"].clear()

def setBoard():
    for i in range(8):
        createPiece("white", "bishop", i, 1)
        createPiece("black", "bishop", i, 6)
    createPiece("white", "pawn", 2, 2)
    createPiece("white", "pawn", 3, 3)
    createPiece("black", "pawn", 5, 2)
    createPiece("black", "pawn", 6, 3)
    createPiece("white", "pawn", 4, 7)

setBoard()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    clearHighlights()

    drawBoard()
    getMouseInfo()
    highlightSquare(mouseFile, mouseRank, hoverColor)
    
    drawSquares()
    drawPieces()
    

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
