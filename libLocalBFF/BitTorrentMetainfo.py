import math
from bencode import bencode
from libLocalBFF import PayloadStreamSegment

def getBitTorrentMetainfoFromBencodedString(metainfo):
    metainfoDict = bencode.bdecode(metainfo)
    
    payloadSize = getPayloadSizeFromMetainfo(metainfoDict)
    
    hashes = getHashesFromMetainfo(metainfoDict)
    
    pieceSize = metainfoDict['info']['piece length']
    finalPieceSize = payloadSize % pieceSize
    
    pieces = []
    numberOfPieces = len(hashes)
    for pieceIndex in range(numberOfPieces-1):
        pieces.append( PayloadStreamSegment.PayloadStreamPiece(size=pieceSize, index=pieceIndex, hash=hashes[pieceIndex]) )
    finalPiece = PayloadStreamSegment.PayloadStreamPiece(size=finalPieceSize, index=(numberOfPieces-1), hash=hashes[-1])
    finalPiece.size = finalPieceSize
    finalPiece.endingStreamOffset = payloadSize
    finalPiece.streamOffset = pieceSize * (numberOfPieces-1)
    pieces.append(finalPiece)
    
    payloadFiles = PayloadStreamSegment.getPayloadStreamFilesFromMetainfo(metainfo=metainfoDict)
    
    return BitTorrentMetainfo(files=payloadFiles, pieceSize=pieceSize, pieces=pieces)

def getMetainfoFileFromPath(path):
    pass
#    with open(path, 'rb') as metainfoFile:
#        rawMetainfo = metainfoFile.read()
#        metainfo = bencode.bdecode(rawMetainfo)
#    
#    if isSingleFileMetainfo(metainfo):
#        metainfo = makeMultipleFileMetainfoFromSingleFileMetainfo(metainfo)
#    
#    files = PayloadFile.getPayloadFilesFromMetainfo(metainfo)
#    hashes = getHashesFromMetainfo(metainfo)

class BitTorrentMetainfo(object):
    
    def __init__(self, files, pieceSize, pieces):
        self.files = files
        self.pieceSize = pieceSize
        self.pieces = pieces
        
        self.payloadSize = self.__getPayloadSize()
        self.finalPieceSize = self.__getFinalPieceSize()
        self.numberOfPieces = self.__getNumberOfPieces()
    
    def __getPayloadSize(self):
        totalSize = 0
        for f in self.files:
            totalSize += f.size
        
        return totalSize

    def __getFinalPieceSize(self):        
        return self.payloadSize % self.pieceSize
    
    def __getNumberOfPieces(self):
        return int(math.ceil(float(self.payloadSize)/self.pieceSize))

#def makeMultipleFileMetainfoFromSingleFileMetainfo(metainfo):
#    alteredMetainfo = dict.copy(metainfo)
#    length = metainfo['info']['length']
#    
#    alteredMetainfo['info']['files'] = [ {'length': length, 'path': []} ]
#    del metainfo
#    return alteredMetainfo

def getHashesFromMetainfo(metainfo):
    concatenatedHashes = metainfo['info']['pieces']
    return splitConcatenatedHashes(concatenatedHashes)

def splitConcatenatedHashes(concatenatedHashes):
    SHA1_HASH_LENGTH = 20
    return [concatenatedHashes[start:start+SHA1_HASH_LENGTH] for start in range(0, len(concatenatedHashes), SHA1_HASH_LENGTH)]

def getPayloadSizeFromMetainfo(metainfo):
    if PayloadStreamSegment.isSingleFileMetainfo(metainfo):
        return metainfo['info']['length']
    else:
        payloadSize = 0
        for f in metainfo['info']['files']:
            payloadSize += f['length']
        return payloadSize