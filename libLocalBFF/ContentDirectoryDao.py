import os
import sqlite3
import logging

def getAllFilesInContentDirectory( contentDirectory ):
  fileInfoFromContentDirectory = []
  
  filesInContentDirectory = 0
  
  for root, dirs, files in os.walk( contentDirectory, onerror=errorEncounteredWhileWalking ):
    for f in files:
      filesInContentDirectory += 1
      filepath = os.path.join( os.path.abspath(root), f )
      
      if os.path.exists( filepath ):
        filesize = os.path.getsize( filepath )
        absolutePath = os.path.abspath( root )
        
        fileInfo = (unicode(absolutePath, errors='replace'), unicode(f, errors='replace'), filesize)
        fileInfoFromContentDirectory.append( fileInfo )
      else:
        logging.error("Problem with accessing file -> " + filepath)
      
      # Errors if the file is a broken link.
#      filesize = os.path.getsize( filepath )
#      absolutePath = os.path.abspath( root )
#      
#      fileInfo = (unicode(absolutePath, errors='replace'), unicode(f, errors='replace'), filesize)
#      fileInfoFromContentDirectory.append( fileInfo )
  
  logging.debug("Total files in content directory -> " + str(filesInContentDirectory))
  dao = ContentDirectoryDao(files=fileInfoFromContentDirectory)
  
  return dao

def errorEncounteredWhileWalking( error ):
  raise error

class ContentDirectoryDao:
  def __init__(self, files=None):
    self.db = sqlite3.connect(":memory:")
    
    cursor = self.db.cursor()
    cursor.execute('''
      create table warez(
        absolute_path text,
        filename text,
        size int
      )
    ''')
    self.db.commit()
    
    if files:
      self.db.executemany("insert into warez values (?,?,?)", files)
      self.db.commit()
  
  def getAllFilesOfSize(self, size):
    cursor = self.db.cursor()
    cursor.execute("select absolute_path, filename from warez where size = ?", (size,))
    filesWithSpecifiedSize = cursor.fetchall()
    
    logging.debug("All files of size " + str(size) + " bytes -> " + str(len(filesWithSpecifiedSize)))
    filenames = []
    for fileInfoRow in filesWithSpecifiedSize:
      fileDirectory = fileInfoRow[0]
      filename = fileInfoRow[1]
      filepath = os.path.join(fileDirectory, filename)
      logging.debug("File: " + filepath)
      filenames.append( filepath )
    
    return filenames
