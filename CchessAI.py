#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class is responsible for managing the artificial intelligence component of 
the Chinese chess game. It will evaluate the current game state, determine the 
optimal moves based on the selected difficulty level, and execute the chosen move. 
It will also maintain a history of the AI's moves throughout the game, enabling 
it to make more informed decisions as the game progresses.
"""

import random

class XiangqiAI:
    def __init__(self, depth):
        self.horseScores = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 2, 2, 2, 2, 2, 2, 2, 1],
                            [1, 2, 4, 3, 3, 3, 4, 2, 1],
                            [1, 2, 3, 3, 3, 3, 3, 2, 1],
                            [1, 2, 3, 5, 5, 5, 3, 2, 1],
                            [1, 2, 3, 5, 5, 5, 3, 2, 1],
                            [1, 2, 2, 3, 3, 3, 3, 2, 1],
                            [1, 2, 4, 3, 3, 3, 4, 2, 1],
                            [1, 2, 2, 2, 2, 2, 2, 2, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
        self.cannonScores = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 2, 2, 2, 2, 2, 2, 2, 1],
                             [2, 2, 3, 3, 5, 3, 3, 2, 2],
                             [1, 2, 3, 3, 4, 3, 3, 2, 1],
                             [1, 2, 3, 5, 6, 5, 3, 2, 1],
                             [1, 2, 3, 5, 5, 5, 3, 2, 1],
                             [1, 2, 3, 3, 4, 3, 3, 2, 1],
                             [2, 2, 3, 3, 6, 3, 3, 2, 2],
                             [1, 2, 2, 2, 2, 2, 2, 2, 1],
                             [1, 1, 1, 1, 1, 1, 1, 2, 1]]

        self.chariotScores = [[1, 2, 2, 2, 1, 2, 2, 2, 1],
                              [1, 2, 2, 2, 2, 2, 2, 2, 1],
                              [1, 3, 2, 3, 3, 3, 2, 3, 1],
                              [1, 2, 3, 3, 3, 3, 3, 3, 1],
                              [1, 2, 3, 4, 4, 4, 3, 2, 1],
                              [1, 2, 3, 4, 4, 4, 3, 2, 1],
                              [1, 2, 2, 3, 3, 3, 3, 3, 1],
                              [1, 3, 2, 3, 3, 3, 2, 3, 1],
                              [2, 2, 2, 2, 2, 2, 2, 2, 2],
                              [1, 2, 2, 1, 1, 1, 2, 2, 1]]

        self.elephantScores = [[0, 0, 2, 0, 0, 0, 2, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 0, 0, 0, 4, 0, 0, 0, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 2, 0, 0, 0, 2, 0, 0],
                               [0, 0, 2, 0, 0, 0, 2, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 0, 0, 0, 4, 0, 0, 0, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 2, 0, 0, 0, 2, 0, 0]]

        self.advisorScores = [[0, 0, 0, 2, 0, 2, 0, 0, 0],
                              [0, 0, 0, 0, 3, 0, 0, 0, 0],
                              [0, 0, 0, 1, 0, 1, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1, 0, 1, 0, 0, 0],
                              [0, 0, 0, 0, 3, 0, 0, 0, 0],
                              [0, 0, 0, 2, 0, 2, 0, 0, 0]]

        self.redSoldierScores = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 2, 2, 5, 6, 5, 2, 2, 1],
                                 [3, 3, 4, 5, 5, 5, 4, 3, 3],
                                 [3, 4, 4, 3, 4, 3, 4, 4, 3],
                                 [3, 3, 3, 3, 3, 3, 3, 3, 3],
                                 [2, 2, 2, 2, 1, 2, 2, 2, 2],
                                 [1, 0, 1, 0, 1, 0, 1, 0, 1],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.blackSoldierScores = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [1, 0, 1, 0, 1, 0, 1, 0, 1],
                                   [2, 2, 2, 2, 1, 2, 2, 2, 2],
                                   [3, 3, 3, 3, 3, 3, 3, 3, 3],
                                   [3, 4, 4, 3, 4, 3, 4, 4, 3],
                                   [3, 3, 4, 5, 5, 5, 4, 3, 3],
                                   [1, 2, 2, 5, 6, 5, 2, 2, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
        self.__pieceScore = {"K": 0, "R": 9, "H": 5, "C": 7, "A": 3, "E": 3, "S": 1}
        self._CHECKMATE = 1000
        self._STALEMATE = 0
        self._counter = 0

        self.piecePositionScores = {"H": self.horseScores, "R": self.chariotScores, "C": self.cannonScores,
                                    "E": self.elephantScores, "A": self.advisorScores,
                                    "RS": self.redSoldierScores, "BS": self.blackSoldierScores}
        
        self.DEPTH = depth
        self.nextMove = None
        
    def findRandomMove(self, validMoves):
        return validMoves[random.randint(0, len(validMoves) - 1)]

    def findBestMove(self, gs, validMoves):
        random.shuffle(validMoves)
        self.findMoveMiniMaxAlphaBeta(gs, validMoves, self.DEPTH, -self._CHECKMATE, self._CHECKMATE, 1 if gs.redToMove else -1)
        print("No. of search for this move:",self._counter)
        return self.nextMove

    def findMoveMiniMaxAlphaBeta(self, gs, validMoves, depth, alpha, beta, turnMultiplier):
        self._counter += 1
        if depth == 0:  # back the root
            return turnMultiplier * self.__scoreBoard(gs)

        maxScore = -self._CHECKMATE
        for move in validMoves:  # loop every single valid move
            gs.makeMove(move)
            nextMoves = gs.getValidMoves() # create a subtree
            score = -self.findMoveMiniMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == self.DEPTH:
                    self.nextMove = move
                    print(move, -score)  # print thh AI thinking process
            gs.undoMove()
            
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:  # pruning happen when alpha >= beta
                break
        return maxScore

    def __scoreBoard(self, gs):
        if gs.checkMate:
            if gs.redToMove:
                return -self._CHECKMATE
            else:
                return self._CHECKMATE
        elif gs.staleMate:
            return self._STALEMATE

        score = 0
        for row in range(len(gs.board)):
            for col in range(len(gs.board[row])):
                square = gs.board[row][col]
                if square != "--":  # square is not empty
                    piecePositionScore = 0
                    if square[1] != "K":  # piece is not general
                        if square[1] == "S":  # for pawns
                            piecePositionScore = self.piecePositionScores[square][row][col]
                        else: 
                            piecePositionScore = self.piecePositionScores[square[1]][row][col]
                    score += self.__pieceScore[square[1]] * (1 if square[0] == 'R' else -1) + piecePositionScore * (.5 if square[0] == 'R' else -.5)
        return score

