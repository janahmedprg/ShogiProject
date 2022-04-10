import os
import piece
import copy

class Board:
    """
    Class that represents the BoxShogi board
    """

    # The BoxShogi board is 5x5
    BOARD_SIZE = 5

    def __init__(self):
        self._board = self._initEmptyBoard()

    def _initEmptyBoard(self):
        return [ ['']*self.BOARD_SIZE for i in range(self.BOARD_SIZE)]

    def __repr__(self):
        return self._stringifyBoard()

    def placePieces(self, pieces):
        self._board = self._initEmptyBoard()
        for p in pieces:
            if p.xPos < 0:
                continue
            self._board[p.xPos][p.yPos] = p.pType
        for p in pieces:
            p.validMoves = self.validPieceMoves(p.xPos, p.yPos)
        return pieces

    def placePiece(self, xPos, yPos, xTarget, yTarget):
        self._board[xTarget][yTarget] = self._board[xPos][yPos]
        self._board[xPos][yPos] = ''


    def movePiece(self, xPos, yPos, xTarget, yTarget, pieces, playerTurn):
        if self._board[xPos][yPos] == '':
            return []

        if playerTurn.isupper() != self._board[xPos][yPos].isupper():
            return []

        if (self._board[xTarget][yTarget] != '') and (playerTurn.isupper() == self._board[xTarget][yTarget].isupper()):
            return []

        for p in pieces:
            if p.pType == self._board[xPos][yPos]:
                if not ((xTarget,yTarget) in p.validMoves):
                    return []

        pieces = piece.setPiecePosition(pieces, self._board[xPos][yPos], xTarget, yTarget)

        self.placePiece(xPos, yPos, xTarget, yTarget)

        pieces = self.updateValidMoves(pieces, xPos, yPos, xTarget, yTarget)

        return pieces

    def _stringifyBoard(self):
        """
        Utility function for printing the board
        """
        s = ''
        for row in range(len(self._board) - 1, -1, -1):

            s += '' + str(row + 1) + ' |'
            for col in range(0, len(self._board[row])):
                s += self._stringifySquare(self._board[col][row])

            s += os.linesep

        s += '    a  b  c  d  e' + os.linesep
        return s

    def _stringifySquare(self, sq):
        """
       	Utility function for stringifying an individual square on the board
        :param sq: Array of strings.
        """
        if type(sq) is not str or len(sq) > 2:
            raise ValueError('Board must be an array of strings like "", "P", or "+P"')
        if len(sq) == 0:
            return '__|'
        if len(sq) == 1:
            return ' ' + sq + '|'
        if len(sq) == 2:
            return sq + '|'

    def updateValidMoves(self, pieces, xPos, yPos, xTarget, yTarget):
        for p in pieces:
            if (xTarget, yTarget) in p.validMoves or (xPos, yPos) in p.validMoves:
                p.validMoves = self.validPieceMoves(p.xPos, p.yPos)
        return pieces

    def movesOutOfCheck(self, pieces, drive):
        atkPieces = []
        for p in pieces:
            if p.pType.isupper() == drive.pType.isupper():
                continue
            if (drive.xPos,drive.yPos) in p.validMoves:
                atkPieces.append(p)
        availableMoves = []
        if len(atkPieces) == 1:
            distance = (atkPieces[0].xPos - drive.xPos, atkPieces[0].yPos - drive.yPos)
            if 1 in distance or -1 in distance:
                for aMove in drive.validMoves:
                    if self._board[aMove[0]][aMove[1]] !='' and self._board[aMove[0]][aMove[1]].isupper() == drive.pType.isupper():
                        continue
                    b = copy.deepcopy(self)
                    ps = copy.deepcopy(pieces)
                    ps = piece.setPiecePosition(ps, drive.pType, aMove[0], aMove[1])
                    b.placePiece(drive.xPos, drive.yPos, aMove[0], aMove[1])
                    ps = self.updateValidMoves(ps, drive.xPos, drive.yPos, aMove[0], aMove[1])
                    check = b.checkForCheck(ps, piece.getPiece(ps, drive.pType))
                    if not check:
                        availableMoves.append([(drive.xPos, drive.yPos),aMove])
                for p in pieces:
                    if p.pType == drive.pType:
                        continue
                    if p.pType.isupper() == drive.pType.isupper() and (atkPieces[0].xPos,atkPieces[0].yPos) in p.validMoves:
                        b = copy.deepcopy(self)
                        ps = copy.deepcopy(pieces)
                        ps = piece.setPiecePosition(ps, p.pType, atkPieces[0].xPos,atkPieces[0].yPos)
                        b.placePiece(p.xPos, p.yPos, atkPieces[0].xPos,atkPieces[0].yPos)
                        ps = self.updateValidMoves(ps, p.xPos, p.yPos, atkPieces[0].xPos,atkPieces[0].yPos)
                        check = b.checkForCheck(ps, piece.getPiece(ps, p.pType))
                        if not check:
                            availableMoves.append([(p.xPos, p.yPos),(atkPieces[0].xPos, atkPieces[0].yPos)])
            elif 0 in distance:
                for aMove in drive.validMoves:
                    if self._board[aMove[0]][aMove[1]] !='' and self._board[aMove[0]][aMove[1]].isupper() == drive.pType.isupper():
                        continue
                    b = copy.deepcopy(self)
                    ps = copy.deepcopy(pieces)
                    ps = piece.setPiecePosition(ps, drive.pType, aMove[0], aMove[1])
                    b.placePiece(drive.xPos, drive.yPos, aMove[0], aMove[1])
                    ps = self.updateValidMoves(ps, drive.xPos, drive.yPos, aMove[0], aMove[1])
                    check = b.checkForCheck(ps, piece.getPiece(ps, drive.pType))
                    if not check:
                        availableMoves.append([(drive.xPos, drive.yPos),aMove])
                if distance[0] == 0:
                    travel = distance[1]
                    if travel>0:
                        trange = list(range(travel))
                    else:
                        trange = list(range(0,travel,-1))
                    for t in trange:
                        for p in pieces:
                            if p.pType == drive.pType:
                                continue
                            if p.pType.isupper() == drive.pType.isupper() and (atkPieces[0].xPos,atkPieces[0].yPos+t) in p.validMoves:
                                b = copy.deepcopy(self)
                                ps = copy.deepcopy(pieces)
                                ps = piece.setPiecePosition(ps, p.pType, atkPieces[0].xPos,atkPieces[0].yPos+t)
                                b.placePiece(p.xPos, p.yPos, atkPieces[0].xPos,atkPieces[0].yPos+t)
                                ps = self.updateValidMoves(ps, p.xPos, p.yPos, atkPieces[0].xPos,atkPieces[0].yPos+t)
                                check = b.checkForCheck(ps, piece.getPiece(ps, p.pType))
                                if not check:
                                    availableMoves.append([(p.xPos, p.yPos),(atkPieces[0].xPos, atkPieces[0].yPos+t)])
                else:
                    travel = distance[0]
                    if travel>0:
                        trange = list(range(travel))
                    else:
                        trange = list(range(0,travel,-1))
                    for t in trange:
                        for p in pieces:
                            if p.pType == drive.pType:
                                continue
                            if p.pType.isupper() == drive.pType.isupper() and (atkPieces[0].xPos+t,atkPieces[0].yPos) in p.validMoves:
                                b = copy.deepcopy(self)
                                ps = copy.deepcopy(pieces)
                                ps = piece.setPiecePosition(ps, p.pType, atkPieces[0].xPos+t,atkPieces[0].yPos)
                                b.placePiece(p.xPos, p.yPos, atkPieces[0].xPos+t,atkPieces[0].yPos)
                                ps = self.updateValidMoves(ps, p.xPos, p.yPos, atkPieces[0].xPos+t,atkPieces[0].yPos)
                                check = b.checkForCheck(ps, piece.getPiece(ps, p.pType))
                                if not check:
                                    availableMoves.append([(p.xPos, p.yPos),(atkPieces[0].xPos+t, atkPieces[0].yPos)])
            else:
                for aMove in drive.validMoves:
                    if self._board[aMove[0]][aMove[1]] !='' and self._board[aMove[0]][aMove[1]].isupper() == drive.pType.isupper():
                        continue
                    b = copy.deepcopy(self)
                    ps = copy.deepcopy(pieces)
                    ps = piece.setPiecePosition(ps, drive.pType, aMove[0], aMove[1])
                    b.placePiece(drive.xPos, drive.yPos, aMove[0], aMove[1])
                    ps = self.updateValidMoves(ps, drive.xPos, drive.yPos, aMove[0], aMove[1])
                    check = b.checkForCheck(ps, piece.getPiece(ps, drive.pType))
                    if not check:
                        availableMoves.append([(drive.xPos, drive.yPos),aMove])
                xtravel = distance[0]
                ytravel = distance[1]
                if xtravel>0:
                    xtrange = list(range(xtravel))
                else:
                    xtrange = list(range(0,xtravel,-1))
                if ytravel>0:
                    ytrange = list(range(ytravel))
                else:
                    ytrange = list(range(0,ytravel,-1))
                for xt,yt in zip(xtrange, ytrange):
                    for p in pieces:
                        if p.pType == drive.pType:
                            continue
                        if p.pType.isupper() == drive.pType.isupper() and (atkPieces[0].xPos-xt,atkPieces[0].yPos-yt) in p.validMoves:
                            b = copy.deepcopy(self)
                            ps = copy.deepcopy(pieces)
                            ps = piece.setPiecePosition(ps, p.pType, atkPieces[0].xPos-xt,atkPieces[0].yPos-yt)
                            b.placePiece(p.xPos, p.yPos, atkPieces[0].xPos-xt,atkPieces[0].yPos-yt)
                            ps = self.updateValidMoves(ps, p.xPos, p.yPos, atkPieces[0].xPos-xt,atkPieces[0].yPos-yt)
                            for pp in ps:
                                print(pp.pType, pp.validMoves)
                            check = b.checkForCheck(ps, drive)
                            if not check:
                                availableMoves.append([(p.xPos, p.yPos),(atkPieces[0].xPos-xt, atkPieces[0].yPos-yt)])
        else:
            for aMove in drive.validMoves:
                if self._board[aMove[0]][aMove[1]] !='' and self._board[aMove[0]][aMove[1]].isupper() == drive.pType.isupper():
                    continue
                b = copy.deepcopy(self)
                ps = copy.deepcopy(pieces)
                ps = piece.setPiecePosition(ps, drive.pType, aMove[0], aMove[1])
                b.placePiece(drive.xPos, drive.yPos, aMove[0], aMove[1])
                ps = self.updateValidMoves(ps, drive.xPos, drive.yPos, aMove[0], aMove[1])
                check = b.checkForCheck(ps, piece.getPiece(ps, drive.pType))
                if not check:
                    availableMoves.append([(drive.xPos, drive.yPos),aMove])

        return availableMoves

    def checkForCheck(self, pieces, drive):
        for p in pieces:
            if p.pType.isupper() == drive.pType.isupper():
                continue
            if (drive.xPos,drive.yPos) in p.validMoves:
                return True
        return False

    def validPieceMoves(self, xPos, yPos):
        validMoves = []
        isUpper = self._board[xPos][yPos].isupper()
        if self._board[xPos][yPos].upper() == 'D':
            for i in range(-1,2):
                for j in range(-1,2):
                    if i == 0 and j == 0:
                        continue
                    newXPos = xPos + i
                    newYPos = yPos + j
                    if (newXPos<0 or newXPos>4) or (newYPos<0 or newYPos>4):
                        continue
                    validMoves.append((newXPos, newYPos))

        elif self._board[xPos][yPos].upper() == 'N':
            for i in range(1,5):
                newXPos = xPos + i
                newYPos = yPos
                if newXPos > 4:
                    break
                if (self._board[newXPos][newYPos] != ''):
                    validMoves.append((newXPos, newYPos))
                    break
                validMoves.append((newXPos, newYPos))
            for i in range(1,5):
                newXPos = xPos
                newYPos = yPos + i
                if newYPos > 4:
                    break
                if (self._board[newXPos][newYPos] != ''):
                    validMoves.append((newXPos, newYPos))
                    break
                validMoves.append((newXPos, newYPos))
            for i in range(1,5):
                newXPos = xPos - i
                newYPos = yPos
                if newXPos < 0:
                    break
                if (self._board[newXPos][newYPos] != ''):
                    validMoves.append((newXPos, newYPos))
                    break
                validMoves.append((newXPos, newYPos))
            for i in range(1,5):
                newXPos = xPos
                newYPos = yPos - i
                if newYPos < 0:
                    break
                if (self._board[newXPos][newYPos] != ''):
                    validMoves.append((newXPos, newYPos))
                    break
                validMoves.append((newXPos, newYPos))

        elif self._board[xPos][yPos].upper() == 'G':
            for i in range(1,5):
                newXPos = xPos + i
                newYPos = yPos + i
                if newXPos > 4:
                    break
                if newYPos > 4:
                    break
                if (self._board[newXPos][newYPos] != ''):
                    validMoves.append((newXPos, newYPos))
                    break
                validMoves.append((newXPos, newYPos))
            for i in range(1,5):
                newXPos = xPos + i
                newYPos = yPos - i
                if newXPos > 4:
                    break
                if newYPos > 4:
                    break
                if newXPos < 0:
                    break
                if newYPos < 0:
                    break
                if (self._board[newXPos][newYPos] != ''):
                    validMoves.append((newXPos, newYPos))
                    break
                validMoves.append((newXPos, newYPos))
            for i in range(1,5):
                newXPos = xPos - i
                newYPos = yPos - i
                if newXPos < 0:
                    break
                if newYPos < 0:
                    break
                if (self._board[newXPos][newYPos] != ''):
                    validMoves.append((newXPos, newYPos))
                    break
                validMoves.append((newXPos, newYPos))
            for i in range(1,5):
                newXPos = xPos - i
                newYPos = yPos + i
                if newXPos < 0:
                    break
                if newYPos < 0:
                    break
                if newXPos > 4:
                    break
                if newYPos > 4:
                    break
                if (self._board[newXPos][newYPos] != ''):
                    validMoves.append((newXPos, newYPos))
                    break
                validMoves.append((newXPos, newYPos))

        elif self._board[xPos][yPos].upper() == 'S':
            for i in range(-1,2):
                for j in range(-1,2):
                    if i == 0 and j == 0:
                        continue
                    if i == -1 and j == -1:
                        continue
                    if i == 1 and j == -1:
                        continue
                    if isUpper:
                        newXPos = xPos - i
                        newYPos = yPos - j
                    else:
                        newXPos = xPos + i
                        newYPos = yPos + j
                    if (newXPos<0 or newXPos>4) or (newYPos<0 or newYPos>4):
                        continue
                    validMoves.append((newXPos, newYPos))
        elif self._board[xPos][yPos].upper() == 'R':
            for i in range(-1,2):
                if isUpper:
                    newXPos = xPos - i
                    newYPos = yPos - 1
                else:
                    newXPos = xPos + i
                    newYPos = yPos + 1
                if (newXPos<0 or newXPos>4) or (newYPos<0 or newYPos>4):
                    continue
                validMoves.append((newXPos, newYPos))
            for i in range(-1,2,2):
                if isUpper:
                    newXPos = xPos + i
                    newYPos = yPos + 1
                else:
                    newXPos = xPos - i
                    newYPos = yPos -1
                if (newXPos<0 or newXPos>4) or (newYPos<0 or newYPos>4):
                    continue
                validMoves.append((newXPos, newYPos))
        elif self._board[xPos][yPos].upper() == 'P':
            if isUpper:
                newXPos = xPos
                newYPos = yPos - 1
            else:
                newXPos = xPos
                newYPos = yPos + 1

            if (newXPos<0 or newXPos>4) or (newYPos<0 or newYPos>4):
                return validMoves
            validMoves.append((newXPos, newYPos))

        return validMoves
