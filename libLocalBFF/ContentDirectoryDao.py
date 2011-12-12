import os
import sqlite3

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
        print("Problem with accessing file -> " + filepath)
      
  print("Total files in content directory -> " + str(filesInContentDirectory))
  dao = ContentDirectoryDao(files=fileInfoFromContentDirectory)
  
  return dao

def errorEncounteredWhileWalking( error ):
  print "Error accessing path:"
  print "  '" + error.filename + "'"
  print error
  print "To fix this problem, perhaps execute the following command:"
  print " # chmod -R +rx '" + error.filename + "'"

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
    
    print("All files of size " + str(size) + " bytes -> " + str(len(filesWithSpecifiedSize)))
    filenames = []
    for fileInfoRow in filesWithSpecifiedSize:
      fileDirectory = fileInfoRow[0]
      filename = fileInfoRow[1]
      filepath = os.path.join(fileDirectory, filename)

      if os.access(filepath, os.R_OK):
        print "File added: " + filepath
        filenames.append( filepath )
      else:
        print "Cannot read file due to permissions error, ignoring:"
        print "  '" + filepath + "'"
        print "To fix this problem, perhaps execute the following command:"
        print " # chmod +r '" + filepath + "'"
    
    return filenames
