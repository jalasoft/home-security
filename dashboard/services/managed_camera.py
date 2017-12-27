from .camera import Camera
from .dircache import DirectoryCache

import logging
import re

class AreaSnapshotFilePattern:
	
    _regexFilePattern_ = r"{}_[^_]+_\.jpg"
    _filenamePattern_ = "{}_%Y-%m-%dT%H:%M.%S_.jpg"
	
    def __init__(self, areaName, managedDir):
        self.name = areaName
        self.managedDir = managedDir
        self.regexFilePattern = self._regexFilePattern_.replace("{}", areaName)
        self.filenaNamePattern = self._filenamePattern_.replace("{}", areaName)
      
    def __str__(self):
        return "AreaFilePattern[" + self.name + ",regex='" + self._regexFilePattern_ + "']"
        
    def fullPath(self):
        from os.path import join
		
        fileName = self.__formatFileName__()
        return join(self.managedDir, fileName)
        
    def __formatFileName__(self):
        import datetime
        today = datetime.datetime.today()
        return today.strftime(self.filenaNamePattern)		

class AreaSnapshotFile:
	
    def __init__(self, path, pattern):
        self.path = path
        self.pattern = pattern
       
    def createdISOTimeString(self):
        from datetime import datetime
        import os
        return datetime.fromtimestamp(os.stat(self.path).st_mtime).isoformat()
        
    def readString(self, encoding="base64"):
        stringContent = self.__readFile__();
        
        if encoding is None:
            return stringContent
            
        if encoding == "base64":
            return self.convertToBase64(stringContent)   
        
        raise ValueError("Unknown encoding '{}'".format(encoding))  
        
        
    def convertToBase64(self, content):
        import base64
        b64Content = base64.b64encode(content)        
        return b64Content
        
    def __readFile__(self):
        with open(self.path, "rb") as fileObject:
            content = fileObject.read()
            return content

class ManagedCamera:

    logger = logging.getLogger("cameraviewer.view")
        
    def __init__(self, managedDir, areaToDeviceMapping):
        self.managedDir = managedDir
        self.areaToDeviceMapping = areaToDeviceMapping
        self.cache = DirectoryCache(managedDir)
        self.camera = Camera()          
        
    
    def capture(self, areaName, refresh):
        if not areaName in self.areaToDeviceMapping:
            raise ValueError("Unknown area '{}'".format(areaName))
		
        area = AreaSnapshotFilePattern(areaName, self.managedDir)
		
        if not refresh:
            self.logger.debug("Taking a snapshot of '" + str(area) + "' from cache.")
            return self.__getFromCache__(area)
        
        self.logger.debug("Taking a fresh snapshot for area '" + str(area) + "'.") 
        self.__takeSnapshot__(area)
        return self.__getFromCache__(area)
        
        	
    def __getFromCache__(self, area):
        
        if area.regexFilePattern in self.cache:
            path = self.cache.latest(area.regexFilePattern)
            return AreaSnapshotFile(path, area)
		
        return self.__takeSnapshot__(area)
        
               
    def __takeSnapshot__(self, area):
        device = self.areaToDeviceMapping[area.name]
        fullPath = area.fullPath()
        self.logger.info("Taking a snapshot from device {0} into file '{1}'.".format(device, fullPath))
        
        path = self.camera.takePicture(device=device, fullPath=fullPath)
        
        self.cache.cleanObsolete(area.regexFilePattern)
        return AreaSnapshotFile(path, area)

    def supportsArea(self, areaName):
        return areaName in self.areaToDeviceMapping
			
