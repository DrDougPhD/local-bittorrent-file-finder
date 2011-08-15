class PayloadStreamSegment(object):
    def __init__(self, size, index):
        self.size = size
        self.index = index

class PayloadStreamPiece(PayloadStreamSegment):
    def __init__(self, size, index):
        PayloadStreamSegment.__init__(self, size=size, index=index)
        
        self.beginningPayloadStreamOffset = size * index

