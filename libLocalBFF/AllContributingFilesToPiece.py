import itertools
from hashlib import sha1

class AllContributingFilesToPiece:
  def __init__(self, listOfContributingFiles=None):
    self.listOfContributingFiles = listOfContributingFiles
    self.combinationProducesPositiveHashMatch = None
  
  def addContributingFile(self, newFile):
    if self.listOfContributingFiles == None:
      self.listOfContributingFiles = []
    
    self.listOfContributingFiles.append(newFile)
  
  def getNumberOfFiles(self):
    return len(self.listOfContributingFiles)
  
  def findCombinationThatMatchesReferenceHash(self, hash):
    cartesianProductOfPossibleFilePathMatches = self.buildCartesianProductOfPossibleFilePathMatches()
    
    print "Processing through all possible file path combinations..."
    print "Worst-case scenario of all combinations to process: " + str( self.getCardinalityOfCartesianProductOfAllPossibleCombinations() )
    print "Files contributing to piece: " + str( self.getNumberOfFiles() )
    
    for combination in cartesianProductOfPossibleFilePathMatches:
      print "Checking combination... "
      print combination
      self.applyCombinationToContributingFiles(combination)
      data = self.getData()
      print "Size of data:\t" + str(len(data))
      print "~"*40
      print "Computed hash:\t" + sha1(data).digest()
      print "Reference hash:\t" + hash
      print "~"*40
      computedHash = sha1(data).digest()
      
      self.combinationProducesPositiveHashMatch = computedHash == hash
      
      if self.combinationProducesPositiveHashMatch:
        print "Combination found!"
        print "#"*40
        self.updateReferenceFilesWithAppropriateMatchedPaths()
        break
      print "#"*40
     
    self.updateStatusOfReferenceFiles()
  
  def buildCartesianProductOfPossibleFilePathMatches(self):
    listOfListOfFilePaths = []
    for contributingFile in self.listOfContributingFiles:
      listOfListOfFilePaths.append(contributingFile.getAllPossibleFilePaths())
    
    print "All possible combinations: "
    print listOfListOfFilePaths
    
    cartesianProduct = itertools.product(*listOfListOfFilePaths)
    return cartesianProduct
  
  def getCardinalityOfCartesianProductOfAllPossibleCombinations(self):
    cardinality = 1
    for contributingFile in self.listOfContributingFiles:
      cardinality *= len(contributingFile.referenceFile.possibleMatches)
    
    return cardinality
  
  def applyCombinationToContributingFiles(self, combination):
    for path, contributingFile in zip(combination, self.listOfContributingFiles):
      print "Applying possible path to file..."
      print "Metafile Path: " +contributingFile.referenceFile.path
      print "Possible match Path: " + path
      contributingFile.possibleMatchPath = path
  
  def getData(self):
    data = ''
    for contributingFile in self.listOfContributingFiles:
      print "Getting data from file: " + contributingFile.possibleMatchPath
      data += contributingFile.getData()
    
    return data
  
  def updateReferenceFilesWithAppropriateMatchedPaths(self):
    for contributingFile in self.listOfContributingFiles:
      contributingFile.applyCurrentMatchPathToReferenceFileAsPositiveMatchPath()
  
  def updateStatusOfReferenceFiles(self):
    status = ''
    
    if self.combinationProducesPositiveHashMatch:
      status = "MATCH_FOUND"
    else:
      status = "CHECKED_WITH_NO_MATCH"
    
    for contributingFile in self.listOfContributingFiles:
      contributingFile.updateStatus(status)
