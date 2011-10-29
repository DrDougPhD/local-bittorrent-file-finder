import utils
import os

def getPayloadFilesFromMetafileDict(metafileDict):
  files = []
  payloadDirectory = metafileDict['info']['name']
  
  if utils.isSingleFileMetafile(metafileDict):
    filename = payloadDirectory
    size = metafileDict['info']['length']
    streamOffset = 0
    
    files.append( PayloadFile(path="", filename=filename, size=size, streamOffset=streamOffset) )
  
  else:
    numberOfFiles = len(metafileDict['info']['files'])
    
    currentStreamOffset = 0
    for i in range(0, numberOfFiles):
      currentFile = metafileDict['info']['files'][i]
      path = os.path.join(payloadDirectory, *currentFile['path'][:-1])
      filename = currentFile['path'][-1]
#      path = payloadDirectory + '/' + '/'.join(currentFile['path'])
      size = currentFile['length']
      index = i
      streamOffset = currentStreamOffset
      
      files.append( PayloadFile(path=path, filename=filename, size=size, streamOffset=streamOffset) )
      
      currentStreamOffset += size
  
  return files

class PayloadFile:
  def __init__(self, path, filename, size, streamOffset):
    self.path = path
    self.filename = filename
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
    return os.path.join(self.path, self.filename)
  
  def getMatchedPathFromContentDirectory(self):
    return self.matchedFilePath
