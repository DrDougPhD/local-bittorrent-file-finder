import unittest
import MetainfoFileHelper
from libLocalBFF import BitTorrentMetainfo

class MetafileElaboratorUnitTest(unittest.TestCase):
    def testConcatenatedHashSplitByEvery20Characters(self):
        NUMBER_OF_HASHES = 3
        HASH_LENGTH = 20
        sampleHashes = MetainfoFileHelper.generateHashList(NUMBER_OF_HASHES)
        expectedHashes = sampleHashes[:]
        hashString = MetainfoFileHelper.getConcatenatedHashesFromList(sampleHashes)
        
        actualHashes = BitTorrentMetainfo.splitConcatenatedHashes(hashString)
        
        self.assertEqual(expectedHashes, actualHashes)
        self.assertEqual(NUMBER_OF_HASHES, len(actualHashes))
        self.assertEqual(HASH_LENGTH, len(actualHashes[0]))
    
    def testFinalPieceSizeCorrectlyCalculatedFromMultiFileMetainfo(self):
        helper = MetainfoFileHelper.MultiFileMetainfoFileHelper()
        expectedFinalPieceSize = helper.finalPieceSize
        
        actualFinalPieceSize = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).getFinalPieceSize()
        
        self.assertEqual( expectedFinalPieceSize, actualFinalPieceSize )
        
    def testFinalPieceSizeCorrectlyCalculatedFromSingleFileMetainfo(self):
        helper = MetainfoFileHelper.SingleFileMetainfoFileHelper()
        expectedFinalPieceSize = helper.finalPieceSize
        
        actualFinalPieceSize = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).getFinalPieceSize()
        
        self.assertEqual( expectedFinalPieceSize, actualFinalPieceSize )
    
    def testPayloadSizeFromMultiFileBitTorrentMetainfo(self):
        helper = MetainfoFileHelper.MultiFileMetainfoFileHelper()
        expectedPayloadSize = helper.payloadSize
        
        actualPayloadSize = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).getPayloadSize()
        
        self.assertEqual( expectedPayloadSize, actualPayloadSize )
    
    def testPayloadSizeFromSingleFileBitTorrentMetainfo(self):
        helper = MetainfoFileHelper.SingleFileMetainfoFileHelper()
        expectedPayloadSize = helper.payloadSize
        
        actualPayloadSize = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).getPayloadSize()
        
        self.assertEqual( expectedPayloadSize, actualPayloadSize )
    
    def testNumberOfPiecesCalculatedFromMultiFileMetainfo(self):
        helper = MetainfoFileHelper.MultiFileMetainfoFileHelper()
        expectedNumberOfPieces = helper.numberOfPieces
        
        actualNumberOfPieces = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).getNumberOfPieces()
        
        self.assertEqual( expectedNumberOfPieces, actualNumberOfPieces )
        
    def testNumberOfPiecesCalculatedFromSingleFileMetainfo(self):
        helper = MetainfoFileHelper.SingleFileMetainfoFileHelper()
        expectedNumberOfPieces = helper.numberOfPieces
        
        actualNumberOfPieces = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).getNumberOfPieces()
        
        self.assertEqual( expectedNumberOfPieces, actualNumberOfPieces )
        
        
if __name__ == '__main__':
    unittest.main()