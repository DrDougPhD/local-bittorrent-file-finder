import unittest
from libLocalBFF import PayloadStreamSegment

class PayloadStreamSegmentTest(unittest.TestCase):

    def testSmoke(self):
        segment = PayloadStreamSegment.PayloadStreamSegment(size=13, index=0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()