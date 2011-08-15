import math
from bencode import bencode
from PayloadFile import PayloadFile

def getBitTorrentMetainfoFromBencodedString(metainfo):
    metainfoDict = bencode.bdecode(metainfo)
    
    pieceSize = metainfoDict['info']['piece length']
    
    payloadFiles = []
    if isSingleFileMetainfo(metainfoDict):
        payloadFiles.append( PayloadFile(path=metainfoDict['info']['name'], length=metainfoDict['info']['length']) )
    else:
        for f in metainfoDict['info']['files']:
            payloadFiles.append( PayloadFile( path = metainfoDict['info']['name'] + "/" + "/".join(f['path']), length=f['length'] ))
    
    return BitTorrentMetainfo(files=payloadFiles, pieceSize=pieceSize)

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
    
    def __init__(self, files, pieceSize):
        self.files = files
        self.pieceSize = pieceSize
        
        self.payloadSize = self.getPayloadSize()
        self.finalPieceSize = self.getFinalPieceSize()
    
    def getPayloadSize(self):
        totalSize = 0
        for f in self.files:
            totalSize += f.length
        
        return totalSize

    def getFinalPieceSize(self):        
        return self.payloadSize % self.pieceSize
    
    def getNumberOfPieces(self):
        return int(math.ceil(float(self.payloadSize)/self.pieceSize))

def isSingleFileMetainfo(metainfo):
    return 'length' in metainfo['info'].keys()

def makeMultipleFileMetainfoFromSingleFileMetainfo(metainfo):
    alteredMetainfo = dict.copy(metainfo)
    length = metainfo['info']['length']
    
    alteredMetainfo['info']['files'] = [ {'length': length, 'path': []} ]
    del metainfo
    return alteredMetainfo

def getHashesFromMetainfo(metainfo):
    concatenatedHashes = metainfo['info']['pieces']
    return splitConcatenatedHashes(concatenatedHashes)

def splitConcatenatedHashes(concatenatedHashes):
    SHA1_HASH_LENGTH = 20
    return [concatenatedHashes[start:start+SHA1_HASH_LENGTH] for start in range(0, len(concatenatedHashes), SHA1_HASH_LENGTH)]
