
from os.path import join
import logging


class SnapshotResolver:

    logger = logging.getLogger("SnapshotResolver")

    __errorMessages__ = [
        "Error opening device",
        "Unable to find a compatible palette",
        "No such file or directory"
        ]

    def isSuccessfull(self, result):
        self.logger.debug("Return code: " + str(result.returncode))
		
        if result.returncode != 0:
            return False

        actualMessage = result.stdout + result.stderr
        actualMessageStr = actualMessage.decode("UTF-8")

        self.logger.debug("Error message: '" + actualMessageStr + "'.")

        for expectedMessage in self.__errorMessages__:
            if expectedMessage in actualMessageStr:
                return False
                
        return True
        
########################################################################
        
class Camera:
  
    logger = logging.getLogger("camera") 
  
    __fswebcam_command_pattern__ = "fswebcam -r 1280x720 --no-banner --device {device} {outputFile}"
    __snapshotResolver__ = SnapshotResolver()

    def takePicture(self, device="/dev/video0", fullPath="~/image.jpg"):
        import datetime
        
        startTime = datetime.datetime.now().timestamp()
        
        while True:
            snapshot = self.__tryTakePicture__(device, fullPath)
            result = self.__snapshotResolver__.isSuccessfull(snapshot)

            if result:
                break

            self.logger.debug("An attempt failed. Retrying....")
            self.__sleep__(2)

        endTime = datetime.datetime.now().timestamp()
        
        self.logger.info("Executed in " + str(round(endTime - startTime)) + " seconds")
        self.logger.info("A new snapshot saved in '" + fullPath + "'.")
        
        return fullPath

    def __prepareDirectory__(self, directory):
        import os
        if directory is ".":
            return os.getcwd()
        else:
            return directory

    def __prepareFileName__(self, name):
        return self.__nowFormatted__().format(name)


    def __tryTakePicture__(self, device, filepath):
        import subprocess
        print("Beru: " + device)
        command = self.__fswebcam_command_pattern__.format(device=device, outputFile=filepath)
        self.logger.debug("Running command '" + command + "'.")
        
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result

    def __sleep__(self, ms):
        import time
        time.sleep(ms)

    def __str__(self):
        return "Camera[fswebcam]"


