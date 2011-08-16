import time
import math
import random
from bencode import bencode

class MetainfoFileHelper(object):
    def __init__(self, payloadLocation):
        self.pieceSize = generateRandomPieceSize()
        self.finalPieceSize = generateRandomFinalPieceSize(self.pieceSize)
        self.numberOfPieces = generateRandomNumberOfPieces()
        
        self.hashes = generateHashList(self.numberOfPieces)
        self.concatenatedHashes = getConcatenatedHashesFromList(self.hashes)
        
        self.payloadSize = generatePayloadSize(self.pieceSize, self.finalPieceSize, self.numberOfPieces)
        
        self.creationDate = int(time.time())
        self.announceUrl = 'http://www.example.com/announce'
        self.payloadLocation = payloadLocation
        
        self.dict = {
                     'info': {
                              'piece length': self.pieceSize,
                              'pieces': self.concatenatedHashes,
                              'name': self.payloadLocation
                              },
                     'announce': self.announceUrl,
                     'creation date': self.creationDate
                     }
    
    def getBencodedMetainfoString(self):
        return bencode.bencode(self.dict)

class SingleFileMetainfoFileHelper(MetainfoFileHelper):
    def __init__(self):
        MetainfoFileHelper.__init__(self, payloadLocation='file')
        
        self.dict['info']['length'] = self.payloadSize

class MultiFileMetainfoFileHelper(MetainfoFileHelper):
    def __init__(self):
        MetainfoFileHelper.__init__(self, payloadLocation='topLevelDirectory')
        
        self.files = generateRandomFilesFromPayloadSize(self.payloadSize)
        self.dict['info']['files'] = self.files 


def generateRandomFilesFromPayloadSize(payloadSize):
    fileSizes = []
    remainingPayloadSize = payloadSize
    while remainingPayloadSize > 0:
        fileSize = random.randint(0, remainingPayloadSize)
        remainingPayloadSize -= fileSize
        fileSizes.append(fileSize)
    
    random.shuffle(fileSizes)
    numberOfFiles = len(fileSizes)
    
    files = []
    for fileIndex in range(0, numberOfFiles):
        filePath = ['insidePayloadDir', 'subDir', 'filename.' + str(fileIndex)]
        size = fileSizes[fileIndex]
        files.append({'length':size, 'path':filePath})
    
    return files

def generateRandomPieceSize():
    TWO_KILOBYTES_POWER_OF_TWO = 11
    EIGHT_MEGABYTES_POWER_OF_TWO = 23
    return int(math.pow(2, random.randint(TWO_KILOBYTES_POWER_OF_TWO, EIGHT_MEGABYTES_POWER_OF_TWO)))

def generateRandomFinalPieceSize(pieceSize):
    return random.randint(1, pieceSize+1)

def generateRandomNumberOfPieces():
    return random.randint(3, 15)

def generateHashList(numberOfHashes):
    return [ "HASHhashHASHhash!!!!" for _ in range(numberOfHashes) ]

def getConcatenatedHashesFromList(hashes):
    return "".join(hashes)

def generatePayloadSize(pieceSize, finalPieceSize, numberOfPieces):
    return (pieceSize * (numberOfPieces - 1)) + finalPieceSize
