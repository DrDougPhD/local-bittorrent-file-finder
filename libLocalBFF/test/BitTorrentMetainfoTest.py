import unittest
import BitTorrentMetainfoHelper
from libLocalBFF import BitTorrentMetainfo

class MetafileElaboratorUnitTest(unittest.TestCase):
    def testSmoke(self):
        metainfo = BitTorrentMetainfo.BitTorrentMetainfo(files=[], pieceSize=2)
            
    def testConcatenatedHashSplitByEvery20Characters(self):
        NUMBER_OF_HASHES = 3
        HASH_LENGTH = 20
        sampleHashes = BitTorrentMetainfoHelper.generateHashList(NUMBER_OF_HASHES)
        expectedHashes = sampleHashes[:]
        hashString = BitTorrentMetainfoHelper.getConcatenatedHashesFromList(sampleHashes)
        
        actualHashes = BitTorrentMetainfo.splitConcatenatedHashes(hashString)
        
        self.assertEqual(expectedHashes, actualHashes)
        self.assertEqual(NUMBER_OF_HASHES, len(actualHashes))
        self.assertEqual(HASH_LENGTH, len(actualHashes[0]))
    
    def testFinalPieceSizeCorrectlyCalculatedFromMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper()
        expectedFinalPieceSize = helper.finalPieceSize
        
        actualFinalPieceSize = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).finalPieceSize
        
        self.assertEqual( expectedFinalPieceSize, actualFinalPieceSize )
        
    def testFinalPieceSizeCorrectlyCalculatedFromSingleFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper()
        expectedFinalPieceSize = helper.finalPieceSize
        
        actualFinalPieceSize = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).finalPieceSize
        
        self.assertEqual( expectedFinalPieceSize, actualFinalPieceSize )
    
    def testPayloadSizeFromMultiFileBitTorrentMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper()
        expectedPayloadSize = helper.payloadSize
        
        actualPayloadSize = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).payloadSize
        
        self.assertEqual( expectedPayloadSize, actualPayloadSize )
    
    def testPayloadSizeFromSingleFileBitTorrentMetainfo(self):
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper()
        expectedPayloadSize = helper.payloadSize
        
        actualPayloadSize = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).payloadSize
        
        self.assertEqual( expectedPayloadSize, actualPayloadSize )
    
    def testNumberOfPiecesCalculatedFromMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper()
        expectedNumberOfPieces = helper.numberOfPieces
        
        actualNumberOfPieces = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).numberOfPieces
        
        self.assertEqual( expectedNumberOfPieces, actualNumberOfPieces )
        
    def testNumberOfPiecesCalculatedFromSingleFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper()
        expectedNumberOfPieces = helper.numberOfPieces
        
        actualNumberOfPieces = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString()).numberOfPieces
        
        self.assertEqual( expectedNumberOfPieces, actualNumberOfPieces )
        
        
if __name__ == '__main__':
    unittest.main()