class PayloadStreamSegment(object):
    def __init__(self, size, index):
        self.size = size
        self.index = index

class PayloadStreamPiece(PayloadStreamSegment):
    def __init__(self, size, index):
        PayloadStreamSegment.__init__(self, size=size, index=index)
        
        self.beginningPayloadStreamOffset = index * size
        self.endingPayloadStreamOffset = (index+1) * size

class PayloadStreamFile(PayloadStreamSegment):
    def __init__(self, size, index, beginningPayloadStreamOffset):
        PayloadStreamSegment.__init__(self, size=size, index=index)
        
        self.beginningPayloadStreamOffset = beginningPayloadStreamOffset
        self.endingPayloadStreamOffset = beginningPayloadStreamOffset + size