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
  metafile = BitTorrentMetafile()
  metafile.files = PayloadFile.getPayloadFilesFromMetafileDict( metafileDict )
  metafile.pieces = PayloadPiece.getPiecesFromMetafileDict( metafileDict )
  
  return metafile

class BitTorrentMetafile:
  def __init__(self, files=None, pieces=None):
    self.files = files
    self.pieces = pieces
