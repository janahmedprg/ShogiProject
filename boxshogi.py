import sys
from utils import parseTestCase
from board import *
from piece import *

def main():
    """
    Main function to read terminal input
    """
    if sys.argv[1] == '-f':
        Input = parseTestCase(sys.argv[2])
        # Prints example output
        print(
"""UPPER player action: drop s d1
5 |__|__| R|__| D|
4 |__|__|__|__|__|
3 |__|__|__|__|__|
2 |__|__|__|__|__|
1 | d| g|__| n|__|
    a  b  c  d  e

Captures UPPER: S R P
Captures lower: p n g s

lower player wins.  Illegal move.""")

    if sys.argv[1] == '-i':
        board = Board()
        pieces = makePieces()
        pieces = board.placePieces(pieces)
        playerTurn = 'lower'
        check = False
        availableMoves = []
        while True:
            print(board)
            if playerTurn.isupper():
                drive = getPiece(pieces, 'D')
            else:
                drive = getPiece(pieces, 'd')

            check = board.checkForCheck(pieces, drive)
            if check:
                print(playerTurn, 'player is in check!')
                availableMoves = board.movesOutOfCheck(pieces, drive)
                print('Available moves:')
                print(availableMoves)

            printCaptures(pieces)

            playerInput = input('\n' + playerTurn + '>')
            if playerInput[0:4] == 'move':
                playerInput = playerInput[5:]
                if not(playerInput[0].upper() >= 'A' and playerInput[0].upper() <= 'E' and playerInput[3].upper() >= 'A' and playerInput[3].upper() <= 'E'):
                    pieces = []
                if not(int(playerInput[1]) >= 1 and int(playerInput[1]) <= 5 and int(playerInput[4]) >= 1 and int(playerInput[4]) <= 5):
                    pieces = []
                xPos = ord(playerInput[0].upper())-65
                yPos = int(playerInput[1])-1
                xTarget = ord(playerInput[3].upper())-65
                yTarget = int(playerInput[4])-1
                if check:
                    for aMove in availableMoves:
                        if (xPos, yPos) == aMove[0] and (xTarget, yTarget) == aMove[1]:
                            check = False
                pieces = board.movePiece(xPos, yPos, xTarget, yTarget, pieces, playerTurn)

            for p in pieces:
                print(p.pType, p.validMoves)        
            if len(pieces) > 0 and not check:
                print(playerTurn + ' player action: ' + playerInput)

            if playerTurn == 'lower':
                playerTurn = 'UPPER'
            else:
                playerTurn = 'lower'

            if len(pieces) == 0 or check:
                print(playerTurn + ' player wins.  Illegal move.')
                return

if __name__ == "__main__":
    main()
