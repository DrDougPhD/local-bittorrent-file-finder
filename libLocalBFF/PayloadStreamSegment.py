class PayloadStreamSegment(object):
    def __init__(self, size, index):
        self.size = size
        self.index = index

class PayloadStreamPiece(PayloadStreamSegment):
    def __init__(self, size, index):
        PayloadStreamSegment.__init__(self, size=size, index=index)
        
        self.streamOffset = index * size
        self.endingStreamOffset = (index+1) * size

class PayloadStreamFile(PayloadStreamSegment):
    def __init__(self, size, index, streamOffset):
        PayloadStreamSegment.__init__(self, size=size, index=index)
        
        self.streamOffset = streamOffset
        self.endingPayloadStreamOffset = streamOffset + size