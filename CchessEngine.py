#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class is responsible for storing all the information about the current state 
of a Chinese chess game. It will also be responsible for determining the valid 
moves at the current state. It will also keep a move log.
"""

class GameState:
    def __init__(self):
        # board is an 10x9 2D list, each element of the list has 2 characters
        # The first character represents the color of the piece, 'B' or 'R'
        # The second character represents the type of piece, 'E','A','C','H','K','R', 'S'
        # '--' - represents an empty space with no piece
        self.board = [
            ["BR", "BH", "BE", "BA", "BK", "BA", "BE", "BH", "BR"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "BC", "--", "--", "--", "--", "--", "BC", "--"],
            ["BS", "--", "BS", "--", "BS", "--", "BS", "--", "BS"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["RS", "--", "RS", "--", "RS", "--", "RS", "--", "RS"],
            ["--", "RC", "--", "--", "--", "--", "--", "RC", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["RR", "RH", "RE", "RA", "RK", "RA", "RE", "RH", "RR"]]
        
        self.__moveFunctions = {'S': self.getSoldierMoves, 'R': self.getChariotMoves, 'H': self.getHorseMoves,
                                'E': self.getElephantMoves, 'A': self.getAdvisorMoves, 'K': self.getGeneralMoves,
                                'C': self.getCannonMoves}
        self.__moveLog = []
        self.__redKingLocation = (9, 4)
        self.__blackKingLocation = (0, 4)
        self.redToMove = True
        self.checkMate = False
        self.staleMate = False
        
    def makeMove(self, move):
        ''' Takes a Move as a parameter and excutes it '''
        self.board[move._startRow][move._startCol] = "--"
        self.board[move._endRow][move._endCol] = move.pieceMoved
        self.__moveLog.append(move) # log the move 
        self.redToMove = not self.redToMove # swap player
        # update the king's location if moved
        if move.pieceMoved == "RK":
            self.__redKingLocation = (move._endRow, move._endCol)
        elif move.pieceMoved == "BK":
            self.__blackKingLocation = (move._endRow, move._endCol)

    def undoMove(self):
        ''' Undo the last move made '''
        if len(self.__moveLog) != 0: # make sure that there is a move to undo
            move = self.__moveLog.pop()
            self.board[move._startRow][move._startCol] = move.pieceMoved
            self.board[move._endRow][move._endCol] = move.pieceCaptured
            self.redToMove = not self.redToMove # switch turns back
            # update the king's location if needed
            if move.pieceMoved == "RK":
                self.__redKingLocation = (move._startRow, move._startCol)
            elif move.pieceMoved == "BK":
                self.__blackKingLocation = (move._startRow, move._startCol)

    def getValidMoves(self):
        ''' All moves considering checks '''
        #1.) generate all possible moves
        moves = self.__getAllPossibleMoves()
        #2.) for each move, make the move
        for i in range(len(moves)-1, -1, -1):  # when removing from a list go backwards through that list
            self.makeMove(moves[i])
            #3.) generate all opponent's moves
            #4.) for each of your opponent's moves, see if they attack your king
            self.redToMove = not self.redToMove
            if self.__inCheck():
                moves.remove(moves[i]) #5.) if they do attack your king, not a valid move
            self.redToMove = not self.redToMove
            self.undoMove()
        if len(moves) == 0:  # either checkmate or stalemate
            if self.__inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves
    
    def __getAllPossibleMoves(self):
        ''' All moves without considering checks '''
        moves = []
        for r in range(len(self.board)):  # number of row
            for c in range(len(self.board[r])):  # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'R' and self.redToMove) or (turn == 'B' and not self.redToMove):
                    piece = self.board[r][c][1]
                    self.__moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece type 
        return moves
    
    def __inCheck(self):
        ''' Determine if the current player is in check '''
        if not self.faceToFace():
            if self.redToMove:
                return self.__squareUnderAttack(self.__redKingLocation[0], self.__redKingLocation[1])
            else:
                return self.__squareUnderAttack(self.__blackKingLocation[0], self.__blackKingLocation[1])
        else:
            return True
    
    def __squareUnderAttack(self, r, c):
        ''' Determine if the enemy can attack the square (r, c) '''
        self.redToMove = not self.redToMove  # switch to opponent's point of view
        oppMoves = self.__getAllPossibleMoves()
        self.redToMove = not self.redToMove  # switch turns back
        for move in oppMoves:
            if move._endRow == r and move._endCol == c:  # square is under attack
                return True
        return False
    
    def faceToFace(self):
        ''' Check if two king is face to face, i.e. in the same Columns with no pieces in between '''
        pieceCount = 0  # counting the piece in one direction
        # start from the one square lower than the black king
        for row in range(self.__blackKingLocation[0]+1, self.__redKingLocation[0]): 
            if self.board[row][self.__redKingLocation[1]] != '--':
                pieceCount += 1
        
        if self.__redKingLocation[1] == self.__blackKingLocation[1] and pieceCount == 0:
            return True
        return False
    
    '''
    Get all the soldier moves for the pawn located at row, col and add these moves to the list
    '''
    def getSoldierMoves(self, r, c, moves):
        '''  (Soldier) moving algorithm 
        1. check the square in front of the soldier if it's empty or it's enemy piece, then adds that move
        2. check if the soldier is over the river, allow it move to left/right if it's over the river
        make this section more clear 
        '''
        allyColor = 'R' if self.redToMove else 'B'
        
        if self.redToMove:  # red soldier moves
            if self.board[r-1][c] != allyColor:  # 1 square advance (empty or enemy)  
                moves.append(Move((r, c), (r-1, c), self.board))
            if 0 <= r < 5: # over the river 
                if c-1 >= 0:
                    if self.board[r][c-1][0] != allyColor: # 1 left square advance
                        moves.append(Move((r, c), (r, c-1), self.board))
                if c+1 < 9:
                    if self.board[r][c+1][0] != allyColor:  # 1 right square advance
                        moves.append(Move((r, c), (r, c+1), self.board))
            
        else:  # black soldier moves
            if r + 1 < 10:  # on board
                if self.board[r+1][c] != allyColor:  # 1 square advance (empty or enemy)
                    moves.append(Move((r, c), (r+1, c), self.board))
            if 5 <= r < 10:  # over the river 
                if c-1 >= 0:
                    if self.board[r][c-1][0] != allyColor:  # 1 left square advance
                        moves.append(Move((r, c), (r, c-1), self.board))
                if c+1 < 9:  
                    if self.board[r][c+1][0] != allyColor:  # 1 right square advance
                        moves.append(Move((r, c), (r, c+1), self.board))
    
    '''
    Get all the chariot moves for the pawn located at row, col and add these moves to the list
    '''
    def getChariotMoves(self, r, c, moves):
        '''  (Chariot) moving algorithm 
        1. check the squares on the given directions that if the squares are on board or not
        2. if these square on board and there's empty or it's enemy piece, then adds that move
        '''
        directions = ((-1,0), (0,-1), (1,0), (0,1)) # up, left, down, right
        enemyColor = 'B' if self.redToMove else 'R'
        for d in directions:
            for i in range(1, 10):
                endRow, endCol = r + d[0] * i, c + d[1] * i
                if 0 <= endRow < 10 and 0 <= endCol < 9:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: break # freindly piece invalid
                else: break  # out of the board

    '''
    Get all the horse moves for the pawn located at row, col and add these moves to the list
    '''
    def getHorseMoves(self, r, c, moves):
        '''  (Horse) moving algorithm    (moving like knight in chess)
        1. check the squares on the given directions that if the squares are on board or not
        2. check if there is a piece next to horse on the way where it moving to 
        '''
        horseMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        allyColor = 'R' if self.redToMove else 'B'
        for m in horseMoves:
            endRow, endCol = r + m[0], c + m[1]
            dx, dy = endRow - r, endCol - c
            blockRow = r if abs(dx)==1 else r+dx//2
            blockCol = c if abs(dy)==1 else c+dy//2
            if 0 <= endRow < 10 and 0 <= endCol < 9:
                endPiece = self.board[endRow][endCol]
                # not an ally piece (empty or enemy), block square is empty
                if endPiece[0] != allyColor and self.board[blockRow][blockCol] == '--': 
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    

    '''
    Get all the elephant moves for the pawn located at row, col and add these moves to the list
    '''
    def getElephantMoves(self, r, c, moves):
        '''  (Elephant) moving algorithm
        1. can only move diagonally behind the reiver, two squares each time 
        1. check the squares on the given directions that if the squares are on board or not
        2. check if there is a piece in the middle of the position where it moving to 
        '''
        directions = ((-2,-2), (-2,2), (2,-2), (2,2))
        allyColor = 'R' if self.redToMove else 'B'
        for d in directions:
            endRow, endCol = r + d[0], c + d[1]
            blockRow, blockCol = r + d[0]//abs(d[0]), c + d[1]//abs(d[1])
            if 0 <= endRow < 10 and 0 <= endCol < 9:  # on board
                if self.redToMove and 5 <= endRow < 10:  # red elephant & behind the river
                    endPiece = self.board[endRow][endCol]
                    # not an ally piece (empty or enemy), block square is empty
                    if endPiece[0] != allyColor and self.board[blockRow][blockCol] == '--':  
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                if not self.redToMove and 0 <= endRow < 5:  # black elephant behind the river
                    endPiece = self.board[endRow][endCol]
                    # not an ally piece (empty or enemy), block square is empty
                    if endPiece[0] != allyColor and self.board[blockRow][blockCol] == '--':  
                        moves.append(Move((r, c), (endRow, endCol), self.board))
        

    '''
    Get all the advisor moves for the pawn located at row, col and add these moves to the list
    '''
    def getAdvisorMoves(self, r, c, moves):
        ''' (Advisor) moving algorithm
        1. can only move diagonally within the red/black palace, one squares each time
        2. check the squares on the given directions that if the squares are on board or not
        '''
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        allyColor = 'R' if self.redToMove else 'B'
        for d in directions:
            endRow, endCol = r + d[0], c + d[1]
            if self.redToMove:
                if 7 <= endRow < 10 and 3 <= endCol < 6:  # on red palace
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
            else:
                if 0 <= endRow < 3 and 3 <= endCol < 6:  # on black palace
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))


    '''
    Get all the cannon moves for the pawn located at row, col and add these moves to the list
    '''
    def getCannonMoves(self, r, c, moves):
        ''' (Cannon) moving algorithm
        1. moving horizontal or vertical as longer as in board
        2. can only capture when there is a piece in between
        '''
        directions = ((-1,0), (0,-1), (1,0), (0,1)) # up, left, down, right
        enemyColor = 'B' if self.redToMove else 'R'
        
        for d in directions:
            pieceCount = 0  # counting the piece in one direction
            for i in range(1, 10):
                endRow, endCol = r + d[0] * i, c + d[1] * i
                if 0 <= endRow < 10 and 0 <= endCol < 9:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" and pieceCount == 0:  # empty square valid 
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # valid capture if there is only a piece in between
                    elif endPiece[0] == enemyColor and pieceCount == 1:  
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    if endPiece != "--":  # pieceCount add one if the square is not empty
                        pieceCount += 1   
                else: break  # out of the board
                
                
    '''
    Get all the General moves for the pawn located at row, col and add these moves to the list
    '''
    def getGeneralMoves(self, r, c, moves):
        ''' (General) moving algorithm
        1. can only move horizontal or vertical within the red/black palace, one squares each time
        2. check the squares on the given directions that if the squares are on board or not
        '''
        kingMoves = ((-1,0), (0,-1), (0,1), (1,0))  # up, left, right, down
        allyColor = 'R' if self.redToMove else 'B'
        for i in range(4):
            endRow, endCol = r + kingMoves[i][0], c + kingMoves[i][1]
            if self.redToMove:
                if 7 <= endRow < 10 and 3 <= endCol < 6:  # on red palace
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
            else:
                if 0 <= endRow < 3 and 3 <= endCol < 6:  # on black palace
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        

class Move:
    # maps keys to values
    # key : value
    ranksToRows = {"1": 9, "2": 8, "3": 7, "4": 6, "5": 5, 
                   "6": 4, "7": 3, "8": 2, "9": 1, "10": 0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4,
                   "f": 5, "g": 6, "h": 7, "i": 8}
    colsToFiles = {v: k for k,v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self._startRow = startSq[0]
        self._startCol = startSq[1]
        self._endRow = endSq[0]
        self._endCol = endSq[1]
        self.pieceMoved = board[self._startRow][self._startCol]
        self.pieceCaptured = board[self._endRow][self._endCol]
        self.isCapture = self.pieceCaptured != "--"
        
        self.moveID = self._startRow * 1000 + self._startCol * 100 + self._endRow * 10 + self._endCol
        
    def __eq__(self, other):
        ''' Overriding the equals method '''
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def __str__(self):
        ''' Overriding the str method '''
        moveString = self.pieceMoved
        if self.isCapture:
            moveString += 'x'
        return moveString + " " + self.getCchessNotation()
    
    def getCchessNotation(self):
        return self.getRankFile(self._startRow, self._startCol) + self.getRankFile(self._endRow, self._endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    

    
    