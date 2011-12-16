import utils
import logging
import FileContributingToPiece
from AllContributingFilesToPiece import AllContributingFilesToPiece
import binascii

module_logger = logging.getLogger(__name__)

def getPiecesFromMetafileDict( metafileDict, files ):
  module_logger.debug("Extracting piece information from metafile dictionary")

  payloadSize = getPayloadSizeFromMetafileDict(metafileDict)
  module_logger.debug('  Payload size => ' + str(payloadSize) + ' Bytes')
  
  hashes = getHashesFromMetafileDict(metafileDict)
  
  pieceSize = getPieceSizeFromDict(metafileDict)
  module_logger.debug('  Piece size => ' + str(pieceSize) + " Bytes")

  finalPieceSize = getFinalPieceSizeFromDict(metafileDict)
  module_logger.debug("  Final piece size => " + str(finalPieceSize) + " Bytes")

  pieces = []
  streamOffset = 0
  numberOfPieces = getNumberOfPiecesFromDict(metafileDict)
  module_logger.debug("  Number of pieces => " + str(numberOfPieces))

  module_logger.debug("  Initializing list of PayloadPieces")
  for pieceIndex in range(numberOfPieces-1):
    module_logger.debug("Constructing piece #" + str(pieceIndex+1))
    piece = PayloadPiece(size=pieceSize, hash=hashes[pieceIndex], streamOffset=streamOffset, index=pieceIndex+1)
    piece.setContributingFilesFromAllFiles(files)
    module_logger.debug(piece.__str__())
    
    pieces.append(piece)
    streamOffset += pieceSize
    module_logger.debug("~"*80)

  module_logger.debug("Constructing piece #" + str(numberOfPieces))
  finalPiece = PayloadPiece(size=finalPieceSize, hash=hashes[-1], streamOffset=streamOffset, index=numberOfPieces)
  finalPiece.setContributingFilesFromAllFiles(files)
  module_logger.debug(finalPiece.__str__())

  pieces.append(finalPiece)

  module_logger.debug("Piece information decoding complete!")
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

def getPieceSizeFromDict(metafileDict):
  return metafileDict['info']['piece length']

def getFinalPieceSizeFromDict(metafileDict):
  return getPayloadSizeFromMetafileDict(metafileDict) % getPieceSizeFromDict(metafileDict)

def getNumberOfPiecesFromDict(metafileDict):
  return len(getHashesFromMetafileDict(metafileDict))

class PayloadPiece:
  def __init__(self, size, streamOffset, hash, index):
    self.size = size
    self.streamOffset = streamOffset
    self.endingOffset = streamOffset+size
    self.hash = hash
    self.index = index
    self.contributingFiles = AllContributingFilesToPiece()

    self.logger = logging.getLogger(__name__)
  
  def __repr__(self):
    return self.__str__()

  def __str__(self):
    output = "PayloadPiece #" + str(self.index) + ":(" + str(self.streamOffset) + "B, " + str(self.endingOffset) + "B) "
    output += "(HASH=" + binascii.b2a_base64(self.hash)[:-1] + ")"
    return output
  
  def setContributingFilesFromAllFiles(self, allFiles):
    self.logger.debug("START: Finding all files contributing to " + self.__str__())
    for payloadFile in allFiles:
      if payloadFile.contributesTo(self):
        contributingFile = FileContributingToPiece.getFromMetafilePieceAndFileObjects(piece=self, file=payloadFile)
        self.contributingFiles.addContributingFile( contributingFile )

    self.logger.debug("END: Finding all files contributing to " + self.__str__())

  def findMatch(self):
    self.logger.debug("Finding all matched files for " + self.__str__())
    self.contributingFiles.findCombinationThatMatchesReferenceHash( hash=self.hash )
    self.logger.debug("~"*80)