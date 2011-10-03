import sys
from libLocalBFF.LocalBitTorrentFileFinder import LocalBitTorrentFileFinder

metafilePath = sys.argv[1]
contentDirectory = sys.argv[2]
service = LocalBitTorrentFileFinder( metafilePath=metafilePath, contentDirectory=contentDirectory )

print "Stage 1: Processing metainfo file..."
print ""
service.processMetafile()
print "Number of Files:\t" + str(service.metafile.numberOfFiles)
print "Payload size:\t\t" + str(service.metafile.payloadSize)
print "Number of Pieces:\t" + str(service.metafile.numberOfPieces)
print "Piece size:\t\t" + str(service.metafile.pieceSize)
print "Final piece size:\t" + str(service.metafile.finalPieceSize)
print ""
print "File descriptions:"
for f in service.metafile.files:
  print "\tPath:\t"+ f.path
  print "\tSize:\t"+ str(f.size)
  print "-"*20

print "Stage 2: Walking content directory..."
print ""
service.gatherAllFilesFromContentDirectory()

print "Stage 3: Finding all file system files that match by size..."
print "#"*40
service.connectFilesInMetafileToPossibleMatchesInContentDirectory()

print "Stage 4: Matching files in the file system to files in metafile..."
service.positivelyMatchFilesInMetafileToPossibleMatches()

for matchedFile in service.files:
  print matchedFile.getPathFromMetafile() + "\t->\t" + matchedFile.getMatchedPathFromContentDirectory()
