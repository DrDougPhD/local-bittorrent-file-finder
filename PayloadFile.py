class PayloadFile(object):
    def __init__(self, path=None, length=None):
        self.path = path
        self.length = length

def getPayloadFilesFromMetainfo(metainfo):
    payloadFiles = []
    for f in metainfo['info']['files']:
        path = metainfo['name'] + "/" + "/".join( f['path'] )
        length = f['length']
        
        payloadFiles.append( PayloadFile(path=path, length=length) )
    
    return payloadFiles