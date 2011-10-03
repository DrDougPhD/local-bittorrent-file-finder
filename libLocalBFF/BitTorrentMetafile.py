from bencode import bencode
import PayloadFile
import PayloadPiece

def getMetafileFromPath( metafilePath ):
  with open( metafilePath, 'rb+' ) as metafile:
    bencodedData = metafile.read()
  
  return getMetafileFromBencodedData( bencodedData )

def getMetafileFromBencodedData( bencodedData ):
  metainfoDict = bencode.bdecode( bencodedData )
  return getMetafileFromDict( metainfoDict )

def getMetafileFromDict( metafileDict ):
  files = PayloadFile.getPayloadFilesFromMetafileDict( metafileDict )
  pieces = PayloadPiece.getPiecesFromMetafileDict( metafileDict )
  pieceSize = PayloadPiece.getPieceSizeFromDict(metafileDict)
  finalPieceSize = PayloadPiece.getFinalPieceSizeFromDict(metafileDict)
  numberOfPieces = PayloadPiece.getNumberOfPiecesFromDict(metafileDict)
  payloadSize = PayloadPiece.getPayloadSizeFromMetafileDict( metafileDict )
  
  metafile = BitTorrentMetafile(files=files, pieces=pieces, pieceSize=pieceSize, finalPieceSize=finalPieceSize, numberOfPieces=numberOfPieces, payloadSize=payloadSize)
  
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
