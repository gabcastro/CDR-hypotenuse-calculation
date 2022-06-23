import os 
import shutil
import logging

class Management():
    layersImgs = []
    fullPathImgs = []
    fullPathMerged = []

    def __init__(self, dirs: list):
        self.layersDir = (dirs["dirlayer1"], dirs["dirlayer2"])
        self.mergedDir = dirs["dirmerged"]
        self.outDir = dirs["dirout"]

    def run(self):
        self.listImages()
        self.joinPathImgs()
        self.createFullMergePath()
        logging.info("Read and build lists with paths and files")

    def listImages(self):
        """Read a directory and save a colection of images.
        """
        for acDir in self.layersDir:
            self.layersImgs.append(os.listdir(acDir))

    def joinPathImgs(self):
        """Join folder path with the name of each image founded
        """
        fullPathImgs = []

        for idx, actListImg in enumerate(self.layersImgs):
            for actImg in actListImg:
                fullPathImgs.append(self.layersDir[idx] + '/' + actImg)

        fullPathImgsL1 = fullPathImgs[0:int(len(fullPathImgs)/2)]
        fullPathImgsL2 = fullPathImgs[int(len(fullPathImgs)/2):len(fullPathImgs)]

        self.fullPathImgs.append(fullPathImgsL1)
        self.fullPathImgs.append(fullPathImgsL2)   

    def createFullMergePath(self):
        """Join folder path call 'merged' with the name of files
        """
        for idx, actListImg in enumerate(self.layersImgs):
            for actImg in actListImg:
                self.fullPathMerged.append(self.mergedDir + '/' + actImg)
            break