from bencode import bencode
import PayloadFile

class MetainfoFile(object):
    
    def __init__(self):
        pass

def getMetainfoFileFromPath(path):
    with open(path, 'rb') as metainfoFile:
        rawMetainfo = metainfoFile.read()
        metainfo = bencode.bdecode(rawMetainfo)
    
    if isSingleFileMetainfo(metainfo):
        metainfo = makeMultipleFileMetainfoFromSingleFileMetainfo(metainfo)
    
    files = PayloadFile.getPayloadFilesFromMetainfo(metainfo)
    hashes = getHashesFromMetainfo(metainfo)

def isSingleFileMetainfo(metainfo):
    return 'length' in metainfo['info'].keys()

def makeMultipleFileMetainfoFromSingleFileMetainfo(metainfo):
    alteredMetainfo = dict.copy(metainfo)
    length = metainfo['info']['length']
    
    alteredMetainfo['info']['files'] = [ {'length': length, 'path': []} ]
    del metainfo
    return alteredMetainfo

def getHashesFromMetainfo(metainfo):
    concatenatedHashes = metainfo['info']['pieces']
    return splitConcatenatedHashes(concatenatedHashes)

def splitConcatenatedHashes(concatenatedHashes):
    SHA1_HASH_LENGTH = 20
    return [concatenatedHashes[start:start+SHA1_HASH_LENGTH] for start in range(0, len(concatenatedHashes), 20)]