import unittest
import MetainfoFile

class MetafileElaboratorUnitTest(unittest.TestCase):
    def testConcatenatedHashSplitByEvery20Characters(self):
        expectedHashes = [("1"*20), ("0"*20)]
        sampleConcatenatedHashes = "".join(expectedHashes)
        
        actualHashes = MetainfoFile.splitConcatenatedHashes(sampleConcatenatedHashes)
        
        self.assertEqual( expectedHashes, actualHashes )

if __name__ == '__main__':
    unittest.main()