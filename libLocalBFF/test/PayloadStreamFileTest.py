import unittest
from libLocalBFF import PayloadStreamSegment
import random

class PayloadStreamFileSegmentTest(unittest.TestCase):
    def testSmoke(self):
        payloadFile = PayloadStreamSegment.PayloadStreamFile(path='not/Important', size=19, index=4, streamOffset=2)
    
    def testEndingPayloadStreamOffsetOfFileCalculated(self):
        SAMPLE_FILE_SIZE = random.randint(0, 100)
        SAMPLE_FILE_INDEX = random.randint(0, 20)
        SAMPLE_PAYLOAD_SIZE_TO_CURRENT_FILE = random.randint(0, 10000) 
        expectedEndingPayloadStreamOffset = SAMPLE_PAYLOAD_SIZE_TO_CURRENT_FILE + SAMPLE_FILE_SIZE 
        
        fileSegment = PayloadStreamSegment.PayloadStreamFile(path='not/Important', size=SAMPLE_FILE_SIZE, index=SAMPLE_FILE_INDEX, streamOffset=SAMPLE_PAYLOAD_SIZE_TO_CURRENT_FILE)
        
        actualEndingPayloadStreamOffset = fileSegment.endingStreamOffset
        self.assertEqual(expectedEndingPayloadStreamOffset, actualEndingPayloadStreamOffset)


if __name__ == "__main__":
    unittest.main()