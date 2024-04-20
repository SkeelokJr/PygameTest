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
        pygame.draw.rect(screen, s["color"], s["rect"])

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
        "image": pieceImage,
        "rect": pieceRect
    }
    Pieces.append(pieceData)

def setBoard():
    for i in range(8):
        createPiece("white", "pawn", i, 1)
        createPiece("black", "pawn", i, 6)

def drawPieces():
    for piece in Pieces:
        screen.blit(piece["image"], piece["rect"])

def coordsToFileRank(x, y):
    file = 

def getMouseInfo():
    mousePos = pygame.mouse.get_pos()
    mouseX, mouseY = mousePos[0], mousePos[1]
    mouseFile, mouseRank = 
    print(mouseX, mouseY)

setBoard()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    drawBoard()
    drawSquares()
    drawPieces()
    getMouseInfo()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
