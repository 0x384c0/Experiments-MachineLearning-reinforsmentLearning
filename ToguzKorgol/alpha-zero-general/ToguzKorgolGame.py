import numpy as np

from Game import Game
from ToguzKorgolLogic import Board
from ToguzKorgolLogic import BoardParameters as boardParams

class ToguzKorgolGame(object):
	def __init__(self):
		print "init"
		self.b = Board()

	 def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return boardParams.nnInputForm

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return boardParams.size

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return boardParams.numberOfActions

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player
        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """

        #TODO add nextBoard state generator

        return self.b.nextState(board, player, action)

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player
        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        valids = [0]*self.getActionSize()

        if player == 1:
        	valids = [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0] #TODO add "Туз" logick
        else:
        	valids = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1] #TODO add "Туз" logick


        return np.array(valids)

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """

        #TODO add "ат сыроо" logic

        p1Score = self.b.getPlayerScore(1)
        p2Score = self.b.getPlayerScore(-1)
        if p1Score > boardParams.winScore:
        	return 1
        elif p2Score > boardParams.winScore:
        	return -1
        else:
        	return 0
        

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """

        
        pass #TODO find out what is this

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()
        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """

        
        pass #TODO find out what is this

    def stringRepresentation(self, board):
        """
        Input:
            board: current board
        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """

        return board.tostring()

