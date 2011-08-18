def getPayloadStreamFilesFromMetainfo(metainfo):
    files = []
    payloadDirectory = metainfo['info']['name']
    
    if isSingleFileMetainfo(metainfo):
        path = payloadDirectory
        size = metainfo['info']['length']
        index = 0
        streamOffset = 0
        
        files.append( PayloadStreamFile(path=path, size=size, index=index, streamOffset=streamOffset) )
    else:
        numberOfFiles = len(metainfo['info']['files'])
        
        currentStreamOffset = 0
        for i in range(0, numberOfFiles):
            currentFile = metainfo['info']['files'][i]
            path = payloadDirectory + '/' + '/'.join(currentFile['path'])
            size = currentFile['length']
            index = i
            streamOffset = currentStreamOffset
            
            files.append( PayloadStreamFile(path=path, size=size, index=index, streamOffset=streamOffset) )
            
            currentStreamOffset += size
    
    return files
            
class PayloadStreamSegment(object):
    def __init__(self, size, index):
        self.size = size
        self.index = index

class PayloadStreamPiece(PayloadStreamSegment):
    def __init__(self, size, index, hash):
        PayloadStreamSegment.__init__(self, size=size, index=index)
        
        self.hash = hash
        self.streamOffset = index * size
        self.endingStreamOffset = (index+1) * size

class PayloadStreamFile(PayloadStreamSegment):
    def __init__(self, path, size, index, streamOffset):
        PayloadStreamSegment.__init__(self, size=size, index=index)
        
        self.path = path
        self.streamOffset = streamOffset
        self.endingStreamOffset = streamOffset + size

def isSingleFileMetainfo(metainfo):
    return 'length' in metainfo['info'].keys()