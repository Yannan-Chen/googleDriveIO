from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from glob import glob 
from pathlib import Path

from tqdm.notebook import tqdm, trange
import os
import numpy as np


class googleDriveIO(object):
    def __init__(self):
        gauth = GoogleAuth()           
        self.drive = GoogleDrive(gauth)
        
    def createDriveFolder(self, driveRootID, driveFolderName):

        folder = self.drive.CreateFile({
          'title': driveFolderName,
          'parents': [{'id': driveRootID}],
          'mimeType': 'application/vnd.google-apps.folder'
        })
        folder.Upload()

        return folder

    def uploadFile(self, driveRootID, driveFileName, localFilePath, attempts = 20):
        file = self.drive.CreateFile({'title': driveFileName,
                                  'parents': [{'id':driveRootID}]})
        file.SetContentFile(localFilePath)

        for attempt in range(attempts):
            try:
                file.Upload()
                break
            except:
                time.sleep(0.1)
                if attempts == attempts - 1:
                    print(driveRootID, driveFileName, localFilePath)


        return file

    def recursiveUploading(self, driveRootID, localPath, level = 1):

        allPath = glob(localPath + r'\*')

        for iPath, path in enumerate(tqdm(allPath, leave=False, desc="Level{}".format(level))):
            baseName = os.path.basename(path)

            if os.path.isfile(path):
                file = self.uploadFile(driveRootID, baseName, path)
            else:
                folder = self.createDriveFolder(driveRootID, baseName)
                self.recursiveUploading(folder['id'], path, level+1)
        return