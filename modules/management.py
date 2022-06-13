import os 
import shutil

class Management():
    layersDir = ()
    layersImgs = []
    fullPathImgs = []
    fullPathImgsL1 = []
    fullPathImgsL2 = []
    fullPathMerged = []

    def __init__(self, layerDir : dict, mergeDir : str, tempDir : str):
        self.layersDir = layerDir
        self.mergedDir = mergeDir
        self.tempDir = tempDir

    def run(self):
        self.listImages()
        self.checkIfExistDir(dirSelected=self.mergedDir)
        self.joinPathImgs()
        self.createFullMergePath()

    def listImages(self):
        """Read a directory and save a colection of images.

        Keyword arguments:
        layerDir -- a tuple containing the dir of layer 1 and layer 2 of oct volumes
        """

        for acDir in self.layersDir:
            self.layersImgs.append(os.listdir(acDir))

    def checkIfExistDir(self, dirSelected):
        """Check if exist or not a folder
        
        Conditions:
            True: Folder exist, so will be remove any file in
            False: Create folder

        Keyword arguments:
        dir -- a path 
        """

        if not (os.path.isdir(self.mergedDir)):
            print("Create dir...")
            os.mkdir(dir)
        else:
            print("Recreate dir...")
            shutil.rmtree(self.mergedDir)
            os.mkdir(self.mergedDir)


    def joinPathImgs(self):
        """Join folder path with the name of each image founded
        """
        fullPathImgs = []

        for idx, actListImg in enumerate(self.layersImgs):
            for actImg in actListImg:
                fullPathImgs.append(self.layersDir[idx] + '/' + actImg)

        self.fullPathImgsL1 = fullPathImgs[0:int(len(fullPathImgs)/2)]
        self.fullPathImgsL2 = fullPathImgs[int(len(fullPathImgs)/2):len(fullPathImgs)]

        self.fullPathImgs.append(self.fullPathImgsL1)
        self.fullPathImgs.append(self.fullPathImgsL2)   

    def createFullMergePath(self):
        """Join folder path call 'merged' with the name of files
        """
        for idx, actListImg in enumerate(self.layersImgs):
            for actImg in actListImg:
                self.fullPathMerged.append(self.mergedDir + '/' + actImg)
            break