class Coordinates():

    deeperCoord = []
    leftEdgeCoord = []
    rightEdgeCoord = []

    def __init__(self):
        pass

    def findInnerPoint(self, img):
        """In charge of searching (x, y) deeper in layer 1

        Keyword arguments:
        img -- A numpy array of an image in grayscale
        """
        self.deeperCoord = self.findCoord(img)

    def findEdgePoint(self, img):
        """In charge of searching (x, y) from layer 2, at the edge of the layer

        Keyword arguments:
        img -- A numpy array of an image in grayscale
        """

        # i.e.: an image of 600x600 is divide in two equal parts
        # where the left part will contain pixels from 0 - 300 (x axis)
        # so, the right part will contain 301 - 600 

        halfAxisX = int(img.shape[1]/2)

        self.leftEdgeCoord = self.findCoord(img[0:img.shape[0], 0:halfAxisX])

        self.rightEdgeCoord = self.findCoord(img[0:img.shape[0], halfAxisX:img.shape[1]])
        self.rightEdgeCoord[1] = halfAxisX + self.rightEdgeCoord[1]

    def findCoord(self, img):
        """Generic function that can be used in more than one case, to find a coord.
        """

        bestCoordinate = list([0, 0])

        # shape[0]: hight (y) | shape[1]: width (x)
        for pWidth in range(img.shape[1]): 
            stop = 0
            for pHight in range(img.shape[0]): 
                selectedPixel = img[pHight, pWidth]
                if (selectedPixel in range(238, 255)) and (bestCoordinate[0] < pHight):
                    bestCoordinate = list([pHight, pWidth])
                    stop = 1
                elif (selectedPixel < 200 and (bestCoordinate[0] < pHight) and (stop == 1)):
                    break
        
        return bestCoordinate