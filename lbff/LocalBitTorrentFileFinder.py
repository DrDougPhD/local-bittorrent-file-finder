import BitTorrentMetafile
import ContentDirectoryDao
import logging

class LocalBitTorrentFileFinder:
  def __init__(self, metafilePath=None, contentDirectory=None):
    self.metafilePath = metafilePath
    self.contentDirectory = contentDirectory
    self.logger = logging.getLogger(__name__)
    self.logger.info("LocalBitTorrentFileFinder initialized")
    self.logger.info("  Metafile path     => " + metafilePath)
    self.logger.info("  Content directory => " + contentDirectory)
    
    self.metafile = None
    self.dao = None
    self.files = None
  
  def processMetafile(self):
    self.logger.info("\nStage 1: Processing metainfo file\n---------------------------------")
    self.metafile = BitTorrentMetafile.getMetafileFromPath(self.metafilePath)
  
  def gatherAllFilesFromContentDirectory(self):
    self.logger.info("\nStage 2: Walking content directory\n----------------------------------")
    self.dao = ContentDirectoryDao.getAllFilesInContentDirectory(self.contentDirectory)
 
  def connectFilesInMetafileToPossibleMatchesInContentDirectory(self):
    self.logger.info("\nStage 3: Finding all file system files that match by size\n---------------------------------------------------------")
    if self.dao == None:
      self.gatherAllFilesFromContentDirectory()
    
    self.files = self.metafile.files
    
    for payloadFile in self.files:
      self.logger.debug("Current file:")
      self.logger.debug(payloadFile)
      payloadFile.possibleMatches = self.dao.getAllFilesOfSize( payloadFile.size )
      self.logger.debug("Possible matches: " + str(len(payloadFile.possibleMatches)))
      
  
  def positivelyMatchFilesInMetafileToPossibleMatches(self):
    self.logger.info("\nStage 4: Matching files in the file system to files in metafile\n---------------------------------------------------------------")
    for piece in self.metafile.pieces:
      piece.findMatch()
