from os import listdir, remove, stat
from os.path import isfile, isdir, join
from datetime import timedelta, datetime
import logging

class DirectoryCache:
	
    logger = logging.getLogger("cameraviewer.dircache") 
	
    def __init__(self, dirPath = ".", durabilityDays = 5):
        if not isdir(dirPath):
	        raise ValueError("Directory to be managed must be an existing directory")
	        
        self.dirPath = dirPath
        self.durabilitySeconds = timedelta(days=durabilityDays).total_seconds()

    def __contains__(self, filePattern):
         matchingFiles = self.__listMatchingFiles__(filePattern)
         return len(matchingFiles) > 0

    def __listMatchingFiles__(self, pattern):
        import re       
        regexPattern = re.compile(pattern)    
 
        result = (join(self.dirPath, file) for file in listdir(self.dirPath) if regexPattern.match(file))
		
        return list(result)        
    
    def cleanObsolete(self, pattern):
		
        self.logger.info("Cleaning files older than " + str(self.durabilitySeconds) + " seconds.")
		
        fullPaths = self.__listMatchingFiles__(pattern)
        fullPathsToDelete = list(filter(self.__isObsolete, fullPaths))
        
        self.logger.info("Obsolete files found: " + str(len(fullPathsToDelete)))
        
        for file in fullPathsToDelete:
            self.logger.debug("Deleting file " + file)
            remove(file)  

    def __isObsolete(self, filePath):
        status = stat(filePath)
        createdSeconds = status.st_mtime
        createdDateTime = datetime.fromtimestamp(createdSeconds)
        nowDateTime = datetime.now()
        
        deltaSeconds = (nowDateTime - createdDateTime).total_seconds()
        return deltaSeconds > self.durabilitySeconds
                                     
    def latest(self, pattern):
		
        allMatching = self.__listMatchingFiles__(pattern)
        self.logger.debug("Candidates for selecting the lates snapshots: " + str(allMatching))
        
        latestSnapshot = max(allMatching, key=lambda f: stat(f).st_mtime)
        
        self.logger.info("Latest snapshot matching pattern '" + pattern + "' is: '" + latestSnapshot + "'.")
        return latestSnapshot
        
 



