#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is our main driver file. It will be responsible for handling user input 
and displaying the current GameState object.
"""

from time import time
import sys
import pygame as p
import CchessEngine
import CchessAI

WIDTH = 370
HEIGHT = 410
BOARD_WIDTH = 9 # dimensions of a Chinese chess board are 9x10
BOARD_HEIGHT = 10 

SQ_SIZE = (HEIGHT - 50) // 9
MAX_FPS = 15
IMAGES = {}

def loadImages():
    ''' initialise a global dictionary of images. This will be called exactly once in the main '''
    pieces = ['BR', 'BH', 'BE', 'BA', 'BK', 'BC', 'BS', 'RR', 'RH', 'RE', 'RA', 'RK', 'RC', 'RS']
    for piece in pieces:
        IMAGES[piece] = p.image.load("imgs/" + piece + ".GIF")
    # we can access an image by saying 'IMAGES['RR']
    
def highlightSquares(screen, gs, validMoves, sqSelected):
    ''' Highlight selected piece'''
    if sqSelected != ():
        r, c = sqSelected 
        if gs.board[r][c][0] == ('R' if gs.redToMove else 'B'):  # sqSelected is a piece that can moved
            screen.blit(p.image.load("imgs/OOS.GIF"), (c*SQ_SIZE+7, r*SQ_SIZE+7))  # highlight selected piece 


def drawGameState(screen, gs, validMoves, sqSelected):
    ''' Responsible for all the graphics within a current game state '''
    screen.blit(p.image.load("imgs/WHITE.GIF"), (0,0))
    # add in piece highlighting or move suggestions
    drawPieces(screen, gs.board) # draw pieces on top of those squares
    highlightSquares(screen, gs, validMoves, sqSelected)

def drawPieces(screen, board):
    ''' Draw the pieces on the board using the current GameState.board '''
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            piece = board[r][c]
            if piece != "--":
                # 7 is the distance from the edge of the image to the initial line
                screen.blit(IMAGES[piece], p.Rect((c*SQ_SIZE)+7, (r*SQ_SIZE)+7, SQ_SIZE, SQ_SIZE))

def drawText(screen, text, pos):
    ''' Draw the text '''
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(pos[0], pos[1], WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))   


def gameLoop(p, screen, playerOne, playerTwo, depth):
    ''' The main game loop '''
    clock = p.time.Clock()
    # initialise the chinese chess game itself
    gs = CchessEngine.GameState()
    validMoves = gs.getValidMoves()
    loadImages() # only do this once, before the while loop
    
    gameRound = 0
    sqSelected = () # no square is selected, keep track of the last click of the user (row, col)
    playerClicks = [] # keep track of player clicks (two tuples: [(6, 4), (4, 4)]) 
    moveMade = False # flag variable for when a move is made    
    gameOver = False
    
    while True:
        humanTurn = (gs.redToMove and playerOne) or (not gs.redToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                sys.exit()
                
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() # (x, y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    # the user clicked the same square twice
                    if sqSelected == (row, col) or col >= 9 or row >= 10: 
                        sqSelected = () # deselect
                        playerClicks = [] # clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: # after 2nd click
                        move = CchessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(move)
                                print(move) # debugggg
                                moveMade = True
                                sqSelected = () # reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z and depth == None: # undo when 'z' is pressed and not AI mode
                    gs.undoMove()
                    moveMade = True
                    gameOver = False
                    gameRound -= 2
                if e.key == p.K_r:  # reset the board when 'r' is pressed
                    main()
                
        # AI move finder
        if not gameOver and not humanTurn:
            AI = CchessAI.XiangqiAI(depth)
            t1 = time()
            AIMove = AI.findBestMove(gs, validMoves)
            print("The AI move is:",AIMove)
            t2 = time()
            print('Runtime for this move: %.2f' % (t2 - t1))
            
            if AIMove is None:
                AIMove = AI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
        
        if moveMade:
            gameRound += 1
            print(f"------------ Move {gameRound} ------------")
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen, gs, validMoves, sqSelected)
        # drawFPS(screen, clock)
        
        # game over 
        if gs.checkMate or gs.staleMate:
            drawText(screen, 'Stalemate' if gs.staleMate else 'Black wins by checkmate' if gs.redToMove else 'Red wins by checkmate', (0, 0)) 
            gameOver = True
        elif gameRound >= 200:
            drawText(screen, 'Drawn', (0, 0))
            gameOver = True
            
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawFPS(screen, clock):
    font = p.font.Font(None, 36)
    fps = clock.get_fps()
    fps_text = font.render("FPS: {:.2f}".format(fps), True, (0, 0, 0))
    screen.blit(fps_text, (120, 200))


'''
The main driver for our code. This will handle user input and updating the graphics
Get the pre game setting
'''    
def main():
    # initialise pygame
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chinese Chess")
    clock = p.time.Clock()
    depth = None
    
    selectingMode = True
    selectingAI = False
    while (selectingMode and not selectingAI) or (not selectingMode and selectingAI):
        screen.blit(p.image.load("imgs/WHITE.GIF"), (0,0))

        if selectingMode:  # selecting the game mode
            drawText(screen, "Select game mode", (0,0))
            drawText(screen, "(AI: A, PVP: H)", (5,25))
            for e in p.event.get():
                if e.type == p.QUIT:
                    sys.exit()
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_a:  # Human vs AI mode
                        playerOne = True # True if a human is playing red. If an AI is playing, then false
                        playerTwo = False # Same as above but for black
                        selectingMode = False
                        selectingAI = True
                    elif e.key == p.K_h:
                        playerOne = True # True if a human is playing red. If an AI is playing, then false
                        playerTwo = True # Same as above but for black
                        selectingMode = False
   
        elif selectingAI:  # selecting the AI difficulty if capable
            drawText(screen, "Select the difficulty", (0,0))
            drawText(screen, "(Easy: 1, Medium: 2, Hard: 3)", (5,25))
            for e in p.event.get():
                if e.type == p.QUIT:
                    sys.exit()
                if e.type == p.KEYDOWN:
                    if e.key == p.K_1:
                        depth = 1  # depth = 1 for a easy AI
                        selectingAI = False
                    elif e.key == p.K_2:
                        depth = 2  # depth = 2 for a medium AI
                        selectingAI = False
                    elif e.key == p.K_3:
                        depth = 3  # depth = 3 for a hard AI
                        selectingAI = False
                
        clock.tick(MAX_FPS)
        p.display.flip()
        
    gameLoop(p, screen, playerOne, playerTwo, depth)  # run the game loop 
    
if __name__ == "__main__":
    main()
    
    
    
    