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
    print("Stage 1: Processing metainfo file...")
    self.metafile = BitTorrentMetafile.getMetafileFromPath(self.metafilePath)
    
    print("Number of Files: " + str(self.metafile.numberOfFiles))
    print("Payload size: " + str(self.metafile.payloadSize))
    print("Number of Pieces: " + str(self.metafile.numberOfPieces))
    print("Piece size: " + str(self.metafile.pieceSize))
    print("Final piece size: " + str(self.metafile.finalPieceSize))
    
    print("File descriptions")
    for f in self.metafile.files:
      print("Path: "+ f.getPathFromMetafile())
      print("Size: "+ str(f.size))
  
  def connectFilesInMetafileToPossibleMatchesInContentDirectory(self):
    print("Stage 3: Finding all file system files that match by size...")
    if self.dao == None:
      self.gatherAllFilesFromContentDirectory()
    
    self.files = self.metafile.files
    
    for payloadFile in self.files:
      print("File: " + payloadFile.getPathFromMetafile())
      print("Size: " + str(payloadFile.size))

      payloadFile.possibleMatches = self.dao.getAllFilesOfSize( payloadFile.size )
      print("Possible matches: " + str(len(payloadFile.possibleMatches)))
      
  def gatherAllFilesFromContentDirectory(self):
    print("Stage 2: Walking content directory...")
    self.dao = ContentDirectoryDao.getAllFilesInContentDirectory(self.contentDirectory)
  
  def positivelyMatchFilesInMetafileToPossibleMatches(self):
    print("Stage 4: Matching files in the file system to files in metafile...")
    for piece in self.metafile.pieces:
      piece.findMatch()
