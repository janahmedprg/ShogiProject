class Piece:
    """
    Class that represents a BoxShogi piece
    """

    def __init__(self, pType: str, *args):
        self.pType = pType
        self.xPos = 0
        self.yPos = 0
        self.validMoves = []
        if len(args) > 1:
            self.xPos = args[0]
            self.yPos = args[1]


    def __repr__(self):
        return self.pType

def setPiecePosition(pieces, pieceType, xTargetPos, yTargetPos):
    for p in pieces:
        if p.xPos == xTargetPos and p.yPos == yTargetPos:
            p.xPos = -1
            p.yPos = -1
            p.validMoves = []
            if p.pType[0] == '+':
                p.pType = p.pType[1]
            if p.pType.isupper():
                p.pType = p.pType.lower()
            else:
                p.pType = p.pType.upper()
        if p.pType == pieceType:
            p.xPos = xTargetPos
            p.yPos = yTargetPos
    return pieces

def makePieces():
    lowerPieces = ['d', 's', 'r', 'g', 'n', 'p']
    pieces = []
    for p,i in zip(lowerPieces,range(6)):
        pieces.append(Piece(lowerPieces[i],i%5,0+int(i/5)))
    upperPieces = ['N', 'G', 'R', 'S', 'D', 'P']
    for p,i in zip(upperPieces,range(6)):
        pieces.append(Piece(upperPieces[i],i-int(i/5),4-int(i/5)))
    return pieces

def getPiece(pieces, pType):
    for p in pieces:
        if p.pType == pType:
            return p

def printCaptures(pieces):
    lowerCaptures = ''
    upperCaptures = ''
    for p in pieces:
        if p.pType.isupper() and p.xPos < 0:
            upperCaptures += ' ' + p.pType
        elif (not p.pType.isupper()) and p.xPos < 0:
            lowerCaptures += ' ' + p.pType
    print('Caputeres UPPER:' + upperCaptures)
    print('Caputeres lower:' + lowerCaptures)
