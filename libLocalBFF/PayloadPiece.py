import utils
from hashlib import sha1

def getPiecesFromMetafileDict( metafileDict ):
  payloadSize = getPayloadSizeFromMetafileDict(metafileDict)
  
  hashes = getHashesFromMetafileDict(metafileDict)
  
  pieceSize = metafileDict['info']['piece length']
  finalPieceSize = payloadSize % pieceSize
  
  pieces = []
  streamOffset = 0
  numberOfPieces = len(hashes)
  for pieceIndex in range(numberOfPieces-1):
      pieces.append( PayloadPiece(size=pieceSize, hash=hashes[pieceIndex], streamOffset=streamOffset) )
      streamOffset += pieceSize
  
  finalPiece = PayloadPiece(size=finalPieceSize, hash=hashes[-1])
  finalPiece.size = finalPieceSize
  finalPiece.streamOffset = pieceSize * (numberOfPieces-1)
  pieces.append(finalPiece)
  
  return pieces

def getPayloadSizeFromMetafileDict( metafileDict ):
  if utils.isSingleFileMetafile(metafileDict):
    return metafileDict['info']['length']
  
  else:
    payloadSize = 0
    for f in metafileDict['info']['files']:
        payloadSize += f['length']
    return payloadSize

def getHashesFromMetafileDict(metafileDict):
  concatenatedHashes = metafileDict['info']['pieces']
  return splitConcatenatedHashes(concatenatedHashes)

def splitConcatenatedHashes(concatenatedHashes):
  SHA1_HASH_LENGTH = 20
  return [concatenatedHashes[start:start+SHA1_HASH_LENGTH] for start in range(0, len(concatenatedHashes), SHA1_HASH_LENGTH)]

class PayloadPiece:
  def __init__(self, size=None, hash=None, streamOffset=None):
    self.size = size
    self.hash = hash
    self.streamOffset = streamOffset
    self.file = None
  
  def isMatchedTo( self, possibleMatchedFile ):
    pieceData = self.getDataFromFile( possibleMatchedFile )
    computedHash = sha1( pieceData )
    
    return self.hash == computedHash.digest()
  
  def getDataFromFile( self, possibleMatchedFile ):
    pieceOffsetInFile = self.streamOffset - self.file.streamOffset
    pieceData = None
    with open( possibleMatchedFile, 'rb+' ) as possibleFile:
      possibleFile.seek( pieceOffsetInFile )
      pieceData = possibleFile.read( self.size )
    
    return pieceData
