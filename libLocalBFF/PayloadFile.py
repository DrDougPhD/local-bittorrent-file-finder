import utils

def getPayloadFilesFromMetafileDict(metafileDict):
  files = []
  payloadDirectory = metafileDict['info']['name']
  
  if utils.isSingleFileMetafile(metafileDict):
    path = payloadDirectory
    size = metafileDict['info']['length']
    streamOffset = 0
    
    files.append( PayloadFile(path=path, size=size, streamOffset=streamOffset) )
  
  else:
    numberOfFiles = len(metafileDict['info']['files'])
    
    currentStreamOffset = 0
    for i in range(0, numberOfFiles):
      currentFile = metafileDict['info']['files'][i]
      path = payloadDirectory + '/' + '/'.join(currentFile['path'])
      size = currentFile['length']
      index = i
      streamOffset = currentStreamOffset
      
      files.append( PayloadFile(path=path, size=size, streamOffset=streamOffset) )
      
      currentStreamOffset += size
  
  return files

class PayloadFile:
  def __init__(self, path=None, size=None, streamOffset=None):
    self.path = path
    self.size = size
    self.streamOffset = streamOffset
    self.matchedFile = None
    self.status = "NOT_CHECKED"
  
  def contributesTo(self, piece):   
    fileEndingOffset = self.streamOffset + self.size
    pieceEndingOffset = piece.streamOffset + piece.size
    
    return ( self.streamOffset <= piece.streamOffset and fileEndingOffset >= pieceEndingOffset )
  
  def hasNotBeenMatched(self):
    return not bool( self.matchedFile )
