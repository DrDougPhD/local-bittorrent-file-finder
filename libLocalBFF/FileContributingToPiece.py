from utils import pieceOnlyHasOneFile
from utils import fileBeginsBeforePieceAndEndsInsidePiece
from utils import fileBeginsInsidePieceAndEndsAfterPieceEnds
from utils import fileIsCompletelyHeldInsidePiece

def getFromMetafilePieceAndFileObjects(piece, file):
  byteInWhichFileEndsInPiece = None
  byteInWhichFileBeginsInPiece = None
  
  if pieceOnlyHasOneFile(piece, file):
    print "Piece only has one file"
    byteInWhichFileBeginsInPiece = piece.streamOffset - file.streamOffset
    byteInWhichFileEndsInPiece = piece.size
  elif fileBeginsBeforePieceAndEndsInsidePiece(piece, file):
    print "File begins before piece and ends inside piece"
    byteInWhichFileBeginsInPiece = piece.streamOffset - file.streamOffset
    byteInWhichFileEndsInPiece = file.size - file.streamOffset
  elif fileBeginsInsidePieceAndEndsAfterPieceEnds(piece, file):
    print "File begins inside of piece and ends after piece ends"
    byteInWhichFileBeginsInPiece = 0
    byteInWhichFileEndsInPiece = piece.endingOffset - file.streamOffset
  elif fileIsCompletelyHeldInsidePiece(piece, file):
    print "Entire file is held within piece"
    byteInWhichFileBeginsInPiece = 0
    byteInWhichFileEndsInPiece = file.size
    print "File reference points: "
    print (byteInWhichFileBeginsInPiece, byteInWhichFileEndsInPiece)
  else:
    raise Exception
  
  fcp = FileContributingToPiece(seek=byteInWhichFileBeginsInPiece, read=byteInWhichFileEndsInPiece, referenceFile=file)
  return fcp

class FileContributingToPiece:
  def __init__(self, seek, read, referenceFile, possibleMatchPath=None):
    self.seekOffset = seek
    self.readOffset = read
    self.referenceFile = referenceFile
    self.possibleMatchPath = possibleMatchPath
  
  def getAllPossibleFilePaths(self):
    if self.referenceFile.status == "MATCH_FOUND":
      return [self.referenceFile.matchedFilePath]
    else:
      return self.referenceFile.possibleMatches
  
  def getData(self):
    data = ''
    print "(Offset: " + str(self.seekOffset) + ", Size: " + str(self.readOffset) + ")"
    
    with open(self.possibleMatchPath, 'rb+') as possibleMatchedFile:
      possibleMatchedFile.seek(self.seekOffset)
      data = possibleMatchedFile.read(self.readOffset)
    
    return data
  
  def applyCurrentMatchPathToReferenceFileAsPositiveMatchPath(self):
    self.referenceFile.matchedFilePath = self.possibleMatchPath
  
  def updateStatus(self, status):
    self.referenceFile.status = status
