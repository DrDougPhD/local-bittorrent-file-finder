import BitTorrentMetafile
import ContentDirectoryDao
import logging

class LocalBitTorrentFileFinder:
  def __init__(self, metafilePath=None, contentDirectory=None):
    self.metafilePath = metafilePath
    self.contentDirectory = contentDirectory
    
    self.metafile = None
    self.dao = None
    self.files = None
  
  def processMetafile(self):
    logging.info("Stage 1: Processing metainfo file...")
    self.metafile = BitTorrentMetafile.getMetafileFromPath(self.metafilePath)
    
    logging.debug("Number of Files:\t" + str(self.metafile.numberOfFiles))
    logging.debug("Payload size:\t\t" + str(self.metafile.payloadSize))
    logging.debug("Number of Pieces:\t" + str(self.metafile.numberOfPieces))
    logging.debug("Piece size:\t\t" + str(self.metafile.pieceSize))
    logging.debug("Final piece size:\t" + str(self.metafile.finalPieceSize))
    
    logging.debug("File descriptions")
    for f in self.metafile.files:
      logging.debug("Path:\t"+ f.path)
      logging.debug("Size:\t"+ str(f.size))
  
  def connectFilesInMetafileToPossibleMatchesInContentDirectory(self):
    logging.info("Stage 3: Finding all file system files that match by size...")
    if self.dao == None:
      self.gatherAllFilesFromContentDirectory()
    
    self.files = self.metafile.files
    
    for payloadFile in self.files:
      logging.debug("File: " + payloadFile.path)
      logging.debug("Size: " + str(payloadFile.size))

      payloadFile.possibleMatches = self.dao.getAllFilesOfSize( payloadFile.size )
      logging.debug("Possible matches: " + str(len(payloadFile.possibleMatches)))
      
  def gatherAllFilesFromContentDirectory(self):
    logging.info("Stage 2: Walking content directory...")
    self.dao = ContentDirectoryDao.getAllFilesInContentDirectory(self.contentDirectory)
  
  def positivelyMatchFilesInMetafileToPossibleMatches(self):
    logging.info("Stage 4: Matching files in the file system to files in metafile...")
    for piece in self.metafile.pieces:
      piece.findMatch()
