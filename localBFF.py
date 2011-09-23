import sys

from libLocalBFF import BitTorrentMetafile
from libLocalBFF import ContentDirectoryDao

metafilePath = sys.argv[1]
contentDirectory = sys.argv[2]

metafile = BitTorrentMetafile.getMetafileFromPath(metafilePath)
contentDao = ContentDirectoryDao.getAllFilesInContentDirectory(contentDirectory)

print "Files:\t" + str(len( metafile.files ))
print "Pieces:\t" + str(len( metafile.pieces ))

for piece in metafile.pieces:
  for payloadfile in metafile.files:
    if payloadfile.hasNotBeenMatched():
      if payloadfile.contributesTo(piece):
        piece.beginningOffsetInFile = piece.streamOffset - payloadfile.streamOffset
        piece.file = payloadfile
        possibleMatches = contentDao.getAllFilesOfSize( payloadfile.size )
        
        for possibleMatchedFile in possibleMatches:
          if piece.isMatchedTo( possibleMatchedFile ):
            piece.file.matchedFilePath = possibleMatchedFile          

print "Match info:"
for payloadFile in metafile.files:
  print payloadFile.path + "\t->\t" + payloadFile.matchedFilePath
