import os
import sqlite3

def getAllFilesInContentDirectory( contentDirectory ):
  fileInfoFromContentDirectory = []
  for root, dirs, files in os.walk( contentDirectory ):
    for f in files:
      filepath = os.path.join( root, f )
      filesize = os.path.getsize( filepath )
      absolutePath = os.path.abspath( root )
      
      fileInfo = (unicode(absolutePath, errors='replace'), unicode(f, errors='replace'), filesize)
      fileInfoFromContentDirectory.append( fileInfo )
  
  dao = ContentDirectoryDao(files=fileInfoFromContentDirectory)
  
  return dao

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
        
    filenames = []
    for fileInfoRow in filesWithSpecifiedSize:
      fileDirectory = fileInfoRow[0]
      filename = fileInfoRow[1]
      filepath = os.path.join(fileDirectory, filename)
      filenames.append( filepath )
    
    return filenames