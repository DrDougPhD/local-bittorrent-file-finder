import unittest
import BitTorrentMetainfoHelper
from libLocalBFF import BitTorrentMetainfo
from random import randint

class MetafileElaboratorUnitTest(unittest.TestCase):
    def testSmoke(self):
        metainfo = BitTorrentMetainfo.BitTorrentMetainfo(files=[], pieceSize=2, pieces=None)
            
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
    
    def testFilesPopulatedOnSingleFileMetainfo(self):
        STARTING_BYTE_LOCATION = 0
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper()
        expectedStreamOffsetAtEndOfFile = helper.payloadSize
        expectedStreamOffset = STARTING_BYTE_LOCATION
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        actualStreamOffset = metainfo.files[0].streamOffset
        actualStreamOffsetAtEndOfFile = metainfo.files[0].endingStreamOffset
        
        self.assertEqual( expectedStreamOffset, actualStreamOffset )
        self.assertEqual( expectedStreamOffsetAtEndOfFile, actualStreamOffsetAtEndOfFile )
    
    def testNumberOfFilesPopulatedOnMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper()
        expectedNumberOfFiles = helper.numberOfFiles
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        actualNumberOfFiles = len(metainfo.files)
        
        self.assertEqual( expectedNumberOfFiles, actualNumberOfFiles )
    
    def testFileSizesMatchUpOnMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper()
        numberOfFiles = helper.numberOfFiles
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        for i in range(numberOfFiles):
            expectedCurrentFileSize = helper.files[i]['length']
            actualCurrentFileSize = metainfo.files[i].size
            self.assertEqual( expectedCurrentFileSize, actualCurrentFileSize )
    
    def testFileOffsetsMatchOnMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper()
        numberOfFiles = helper.numberOfFiles
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        expectedStreamOffset = 0
        for i in range(numberOfFiles):
            actualStreamOffset = metainfo.files[i].streamOffset
            self.assertEqual( expectedStreamOffset, actualStreamOffset )
            expectedStreamOffset += helper.files[i]['length']
    
    def testFileEndingOffsetsMatchOnMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper()
        numberOfFiles = helper.numberOfFiles
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        expectedEndingStreamOffset = 0
        for i in range(numberOfFiles):
            expectedEndingStreamOffset += helper.files[i]['length']
            actualEndingStreamOffset = metainfo.files[i].endingStreamOffset
            self.assertEqual( expectedEndingStreamOffset, actualEndingStreamOffset )
            
    def testPieceSizesMatchUpOnSingleFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        expectedPieceSize = helper.pieceSize
        actualPieceSize = metainfo.pieceSize
        self.assertEqual( expectedPieceSize, actualPieceSize )
        
        numberOfPieces = helper.numberOfPieces
        for pieceIndex in range(numberOfPieces-1):
            expectedPieceSize = helper.pieceSize
            actualPieceSize = metainfo.pieces[pieceIndex].size
            self.assertEqual( expectedPieceSize, actualPieceSize )
        
    def testPieceSizesMatchUpOnMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        expectedPieceSize = helper.pieceSize
        actualPieceSize = metainfo.pieceSize
        self.assertEqual( expectedPieceSize, actualPieceSize )
        
        numberOfPieces = helper.numberOfPieces
        for pieceIndex in range(numberOfPieces-1):
            expectedPieceSize = helper.pieceSize
            actualPieceSize = metainfo.pieces[pieceIndex].size
            self.assertEqual( expectedPieceSize, actualPieceSize )
    
    def testFinalPieceSizesMatchUpOnSingleFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        expectedFinalPieceSize = helper.finalPieceSize
        actualFinalPieceSize = metainfo.finalPieceSize
        self.assertEqual(expectedFinalPieceSize, actualFinalPieceSize)
        
        expectedFinalPieceSize = helper.finalPieceSize
        actualFinalPieceSize = metainfo.pieces[-1].size
        self.assertEqual(expectedFinalPieceSize, actualFinalPieceSize)
        
    def testFinalPieceSizesMatchUpOnMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        expectedFinalPieceSize = helper.finalPieceSize
        actualFinalPieceSize = metainfo.finalPieceSize
        self.assertEqual(expectedFinalPieceSize, actualFinalPieceSize)
        
        expectedFinalPieceSize = helper.finalPieceSize
        actualFinalPieceSize = metainfo.pieces[-1].size
        self.assertEqual(expectedFinalPieceSize, actualFinalPieceSize)
    
    def testPieceOffsetForAllPiecesFromSingleFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        pieceSize = helper.pieceSize
        numberOfPieces = helper.numberOfPieces
        expectedStreamOffsetOfCurrentPiece = 0
        for pieceIndex in range(numberOfPieces):
            actualStreamOffsetOfCurrentPiece = metainfo.pieces[pieceIndex].streamOffset
            self.assertEqual( expectedStreamOffsetOfCurrentPiece, actualStreamOffsetOfCurrentPiece )
            expectedStreamOffsetOfCurrentPiece += pieceSize
    
    def testPieceOffsetForAllPiecesFromMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        pieceSize = helper.pieceSize
        numberOfPieces = helper.numberOfPieces
        expectedStreamOffsetOfCurrentPiece = 0
        for pieceIndex in range(numberOfPieces):
            actualStreamOffsetOfCurrentPiece = metainfo.pieces[pieceIndex].streamOffset
            self.assertEqual( expectedStreamOffsetOfCurrentPiece, actualStreamOffsetOfCurrentPiece )
            expectedStreamOffsetOfCurrentPiece += pieceSize
    
    def testPieceEndingOffsetForAllPiecesFromSingleFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        pieceSize = helper.pieceSize
        payloadSize = helper.payloadSize
        
        numberOfPieces = helper.numberOfPieces
        expectedEndingStreamOffsetOfCurrentPiece = 0
        for pieceIndex in range(numberOfPieces-1):
            expectedEndingStreamOffsetOfCurrentPiece += pieceSize
            actualEndingStreamOffsetOfCurrentPiece = metainfo.pieces[pieceIndex].endingStreamOffset
            self.assertEqual( expectedEndingStreamOffsetOfCurrentPiece, actualEndingStreamOffsetOfCurrentPiece )
        expectedEndingStreamOffsetOfCurrentPiece = payloadSize
        actualEndingStreamOffsetOfCurrentPiece = metainfo.pieces[-1].endingStreamOffset
        self.assertEqual( expectedEndingStreamOffsetOfCurrentPiece, actualEndingStreamOffsetOfCurrentPiece )
    
    def testPieceEndingOffsetForAllPiecesFromMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        pieceSize = helper.pieceSize
        payloadSize = helper.payloadSize
        
        numberOfPieces = helper.numberOfPieces
        expectedEndingStreamOffsetOfCurrentPiece = 0
        for pieceIndex in range(numberOfPieces-1):
            expectedEndingStreamOffsetOfCurrentPiece += pieceSize
            actualEndingStreamOffsetOfCurrentPiece = metainfo.pieces[pieceIndex].endingStreamOffset
            self.assertEqual( expectedEndingStreamOffsetOfCurrentPiece, actualEndingStreamOffsetOfCurrentPiece )
        expectedEndingStreamOffsetOfCurrentPiece = payloadSize
        actualEndingStreamOffsetOfCurrentPiece = metainfo.pieces[-1].endingStreamOffset
        self.assertEqual( expectedEndingStreamOffsetOfCurrentPiece, actualEndingStreamOffsetOfCurrentPiece )
    
    def testHashOfEachPieceFromSingleFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.SingleFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        numberOfPieces = helper.numberOfPieces
        for pieceIndex in range(numberOfPieces):
            expectedHash = helper.hashes[pieceIndex]
            actualHash = metainfo.pieces[pieceIndex].hash
            self.assertEqual( expectedHash, actualHash )
            
    def testHashOfEachPieceFromMultiFileMetainfo(self):
        helper = BitTorrentMetainfoHelper.MultiFileMetainfoFileHelper() 
        
        metainfo = BitTorrentMetainfo.getBitTorrentMetainfoFromBencodedString(helper.getBencodedMetainfoString())
        
        numberOfPieces = helper.numberOfPieces
        for pieceIndex in range(numberOfPieces):
            expectedHash = helper.hashes[pieceIndex]
            actualHash = metainfo.pieces[pieceIndex].hash
            self.assertEqual( expectedHash, actualHash )
    
if __name__ == '__main__':
    unittest.main()