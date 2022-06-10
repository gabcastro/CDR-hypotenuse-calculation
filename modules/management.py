import os 

class Management():
    layersDir = ()
    layersImgs = []

    def __init__(self):
        pass

    def listimages(self, layerDir):
        """Read a directory and save a colection of images.

        Keyword arguments:
        layerDir -- a tuple containing the dir of layer 1 and 2
        """

        for acDir in layerDir:
            self.layersImgs.append(os.listdir(acDir))