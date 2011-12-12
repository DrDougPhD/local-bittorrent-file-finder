import sys
from libLocalBFF.LocalBitTorrentFileFinder import LocalBitTorrentFileFinder

metafilePath = sys.argv[1].decode('utf-8')
contentDirectory = sys.argv[2].decode('utf-8')

service = LocalBitTorrentFileFinder( metafilePath=metafilePath, contentDirectory=contentDirectory )

service.processMetafile()

service.gatherAllFilesFromContentDirectory()

service.connectFilesInMetafileToPossibleMatchesInContentDirectory()

service.positivelyMatchFilesInMetafileToPossibleMatches()

for matchedFile in service.files:
  output = ""
  metafilePayloadFilePath = matchedFile.getPathFromMetafile()
  
  if matchedFile.status == 'NOT_CHECKED':
    output = "File not checked"
  elif matchedFile.status == 'MATCH_FOUND':
    output = matchedFile.getMatchedPathFromContentDirectory()
  elif matchedFile.status == 'CHECKED_WITH_NO_MATCH':
    output = "No matches found"
  
  print metafilePayloadFilePath + "\t->\t" + output
