import logging
import utils
import os
import bencode
import PayloadFile
import PayloadPiece
import json

module_logger = logging.getLogger(__name__)

def getMetafileFromPath( metafilePath ):
  module_logger.info("Loading metafile from URI " + metafilePath)
  try:
    with open( metafilePath, 'rb' ) as metafile:
      bencodedData = metafile.read()
      module_logger.debug("File read successfully")
    return getMetafileFromBencodedData( bencodedData )

  except IOError as e:
    module_logger.critical('Metafile is not readible, aborting program.')
    module_logger.critical('Perhaps change the file permissions on "' + metafilePath + '"?')
    module_logger.critical(' # chmod +r "' + metafilePath + '"')
    raise e

def getMetafileFromBencodedData( bencodedData ):
  module_logger.debug("Decoding metafile into python dictionary")
  metainfoDict = bencode.bdecode( bencodedData )

  prunedMetainfoDict = utils.prunedMetainfoDict(metainfoDict)
  module_logger.debug('Decoded metainfo content =>\n' +
    json.dumps(prunedMetainfoDict, indent=2, ensure_ascii=False))

  return getMetafileFromDict( metainfoDict )

def getMetafileFromDict( metafileDict ):
  module_logger.debug("Converting metafile dictionary to BitTorrentMetafile object")
  files = PayloadFile.getPayloadFilesFromMetafileDict( metafileDict )
  pieces = PayloadPiece.getPiecesFromMetafileDict( metafileDict )
  pieceSize = PayloadPiece.getPieceSizeFromDict(metafileDict)
  finalPieceSize = PayloadPiece.getFinalPieceSizeFromDict(metafileDict)
  numberOfPieces = PayloadPiece.getNumberOfPiecesFromDict(metafileDict)
  payloadSize = PayloadPiece.getPayloadSizeFromMetafileDict( metafileDict )
  
  metafile = BitTorrentMetafile(
    files=files,
    pieces=pieces,
    pieceSize=pieceSize, 
    finalPieceSize=finalPieceSize, 
    numberOfPieces=numberOfPieces, 
    payloadSize=payloadSize
  )
  
  return metafile

class BitTorrentMetafile:
  def __init__(self, files, pieces, pieceSize=None, finalPieceSize=None, numberOfPieces=None, payloadSize=None):
    self.files = files
    self.pieces = pieces
    self.pieceSize = pieceSize
    self.finalPieceSize = finalPieceSize
    self.numberOfPieces = numberOfPieces
    self.payloadSize = payloadSize
    
    self.numberOfFiles = len(files)
    
    for piece in self.pieces:
      piece.setContributingFilesFromAllFiles(self.files)

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return "BitTorrent metafile"
