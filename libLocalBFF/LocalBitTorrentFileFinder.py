import BitTorrentMetafile
import ContentDirectoryDao

class LocalBitTorrentFileFinder:
  def __init__(self, metafilePath=None, contentDirectory=None):
    self.metafilePath = metafilePath
    self.contentDirectory = contentDirectory
    
    self.metafile = None
    self.dao = None
    self.files = None
  
  def processMetafile(self):
    self.metafile = BitTorrentMetafile.getMetafileFromPath(self.metafilePath)
  
  def connectFilesInMetafileToPossibleMatchesInContentDirectory(self):
    if self.dao == None:
      self.gatherAllFilesFromContentDirectory()
    
    self.files = self.metafile.files
    
    for payloadFile in self.files:
      print "File:\t\t\t" + payloadFile.path
      print "Size:\t\t\t" + str(payloadFile.size)

      payloadFile.possibleMatches = self.dao.getAllFilesOfSize( payloadFile.size )
      print "Possible matches:\t" + str(len(payloadFile.possibleMatches))
      print "#"*40
      
  def gatherAllFilesFromContentDirectory(self):
    self.dao = ContentDirectoryDao.getAllFilesInContentDirectory(self.contentDirectory)
  
  def positivelyMatchFilesInMetafileToPossibleMatches(self):
    for piece in self.metafile.pieces:
      piece.findMatch()
