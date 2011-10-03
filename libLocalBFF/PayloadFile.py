import utils

def getPayloadFilesFromMetafileDict(metafileDict):
  files = []
  payloadDirectory = metafileDict['info']['name']
  
  if utils.isSingleFileMetafile(metafileDict):
    path = payloadDirectory
    size = metafileDict['info']['length']
    streamOffset = 0
    
    files.append( PayloadFile(path=path, size=size, streamOffset=streamOffset) )
  
  else:
    numberOfFiles = len(metafileDict['info']['files'])
    
    currentStreamOffset = 0
    for i in range(0, numberOfFiles):
      currentFile = metafileDict['info']['files'][i]
      path = payloadDirectory + '/' + '/'.join(currentFile['path'])
      size = currentFile['length']
      index = i
      streamOffset = currentStreamOffset
      
      files.append( PayloadFile(path=path, size=size, streamOffset=streamOffset) )
      
      currentStreamOffset += size
  
  return files

class PayloadFile:
  def __init__(self, path, size, streamOffset):
    self.path = path
    self.size = size
    self.streamOffset = streamOffset
    self.endingOffset = streamOffset+size
    self.matchedFilePath = None
    self.status = "NOT_CHECKED"
  
  def contributesTo(self, piece):   
    fileEndingOffset = self.streamOffset + self.size
    pieceEndingOffset = piece.streamOffset + piece.size
    
    pieceIsWholelyContainedInFile = ( self.streamOffset <= piece.streamOffset and fileEndingOffset >= pieceEndingOffset )

    fileBeginsBeforePieceBegins = self.streamOffset <= piece.streamOffset
    fileEndsAfterPieceBegins = fileEndingOffset > piece.streamOffset
    
    fileBeginsInsidePiece = self.streamOffset < pieceEndingOffset
    fileEndsAfterPieceEnds = fileEndingOffset > pieceEndingOffset
    
    fileIsPartiallyContainedInPiece = (fileBeginsBeforePieceBegins and fileEndsAfterPieceBegins) or (fileBeginsInsidePiece and fileEndsAfterPieceEnds)
    
    
    fileBeginsAfterPieceBegins = self.streamOffset >= piece.streamOffset
    fileEndsBeforePieceEnds = fileEndingOffset <= pieceEndingOffset
    
    fileIsWholelyContainedInPiece = fileBeginsAfterPieceBegins and fileEndsBeforePieceEnds
    
#    if pieceIsWholelyContainedInFile or fileIsWholelyContainedInPiece or fileIsPartiallyContainedInPiece:
#      print "File: " + self.path + " (" + str(self.size) + " bytes)"
#      print "Piece is wholely contained in file? -> " + str( pieceIsWholelyContainedInFile )
#      print "File is partially contained in piece? -> " + str( fileIsPartiallyContainedInPiece )
#      print "File is wholely contained in piece? -> " + str( fileIsWholelyContainedInPiece )
#      print ""
    
    return pieceIsWholelyContainedInFile or fileIsWholelyContainedInPiece or fileIsPartiallyContainedInPiece
  
  def hasNotBeenMatched(self):
    return not bool( self.matchedFilePath )
  
  def getPathFromMetafile(self):
    return self.path
  
  def getMatchedPathFromContentDirectory(self):
    return self.matchedFilePath
