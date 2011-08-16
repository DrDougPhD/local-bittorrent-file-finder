import unittest
from libLocalBFF import PayloadStreamSegment
from libLocalBFF.test import BitTorrentMetainfoHelper


class PayloadStreamPieceUnitTest(unittest.TestCase):
    def testSmoke(self):
        piece = PayloadStreamSegment.PayloadStreamPiece(size=13, index=0)
    
    def testBeginningPayloadStreamOffsetOfPieceCalculated(self):
        SAMPLE_PIECE_SIZE = BitTorrentMetainfoHelper.generateRandomPieceSize()
        SAMPLE_PIECE_INDEX = 1
        expectedBeginningPayloadStreamOffset = SAMPLE_PIECE_INDEX * SAMPLE_PIECE_SIZE
        
        piece = PayloadStreamSegment.PayloadStreamPiece(size=SAMPLE_PIECE_SIZE, index=SAMPLE_PIECE_INDEX)
        
        actualBeginningPayloadStreamOffset = piece.streamOffset
        self.assertEqual(expectedBeginningPayloadStreamOffset, actualBeginningPayloadStreamOffset)
    
    def testEndingPayloadStreamOffsetOfPieceCalculated(self):
        SAMPLE_PIECE_SIZE = BitTorrentMetainfoHelper.generateRandomPieceSize()
        SAMPLE_PIECE_INDEX = 1
        expectedEndingPayloadStreamOffset = (SAMPLE_PIECE_INDEX+1) * SAMPLE_PIECE_SIZE
        
        piece = PayloadStreamSegment.PayloadStreamPiece(size=SAMPLE_PIECE_SIZE, index=SAMPLE_PIECE_INDEX)
        
        actualEndingPayloadStreamOffset = piece.endingStreamOffset
        self.assertEqual(expectedEndingPayloadStreamOffset, actualEndingPayloadStreamOffset)


if __name__ == "__main__":
    unittest.main()