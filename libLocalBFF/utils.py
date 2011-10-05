def isSingleFileMetafile( metafileDict ):
  return 'length' in metafileDict['info'].keys()

def pieceOnlyHasOneFile( piece, file ):
  fileBeginsBeforePieceBegins = file.streamOffset <= piece.streamOffset
  fileEndsAfterPieceEnds = file.endingOffset >= piece.endingOffset
  return fileBeginsBeforePieceBegins and fileEndsAfterPieceEnds

def fileBeginsBeforePieceAndEndsInsidePiece(piece, file):
  fileBeginsBeforePiece = file.streamOffset < piece.streamOffset
  fileEndsInsidePiece = file.endingOffset > piece.streamOffset and file.endingOffset < piece.endingOffset
#  if (fileBeginsBeforePiece and fileEndsInsidePiece):
#    print "-"*20
#    print "File:"
#    print (file.streamOffset, file.endingOffset)
#    print "Piece:"
#    print (piece.streamOffset, piece.endingOffset)  
  return fileBeginsBeforePiece and fileEndsInsidePiece

def fileBeginsInsidePieceAndEndsAfterPieceEnds(piece, file):
  fileBeginsInsidePiece = file.streamOffset > piece.streamOffset and file.streamOffset < piece.endingOffset
  fileEndsAfterPieceEnds = file.endingOffset > piece.endingOffset
  
#  if (fileBeginsInsidePiece and fileEndsAfterPieceEnds):
#    print "-"*20
#    print "File:"
#    print (file.streamOffset, file.endingOffset)
#    print "Piece:"
#    print (piece.streamOffset, piece.endingOffset)
  return fileBeginsInsidePiece and fileEndsAfterPieceEnds

def fileIsCompletelyHeldInsidePiece(piece, file):
  fileBeginsInsidePiece = file.streamOffset >= piece.streamOffset
  fileEndsInsidePiece = file.endingOffset <= piece.endingOffset
  
#  if fileBeginsInsidePiece and fileEndsInsidePiece:
#    print "-"*20
#    print "File:"
#    print (file.streamOffset, file.endingOffset)
#    print "Piece:"
#    print (piece.streamOffset, piece.endingOffset)
  return fileBeginsInsidePiece and fileEndsInsidePiece
