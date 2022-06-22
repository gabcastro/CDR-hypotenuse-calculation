import cv2

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
        # so, the right part will contain 300 - 600 

        halfAxisX = int(img.shape[1]/2)

        self.leftEdgeCoord = self.findCoord(img[0:img.shape[0], 0:halfAxisX])

        self.rightEdgeCoord = self.findCoord(img[0:img.shape[0], halfAxisX:img.shape[1]])
        self.rightEdgeCoord[1] = halfAxisX + self.rightEdgeCoord[1]

    def findDistancesCupRegion(self, img, lcoord, rcoord):
        """In charge of: 
            (1) search for coords between leftEdge and rightEdge, but on the limit of cup area

        Keyword arguments:
        img -- An image to read
        lcoord -- points from left side of the image
        rcoord -- points from right side of the image    

        Returns: 
        Will be return:
            - limits between cup area: two positions (x, y)
        """
        # compute some coords to cut image near from the region where the red line pass
        # x calcs
        xIniPos = lcoord[1]
        xEndPos = rcoord[1]
        lenXPos = xEndPos - xIniPos
        halfXPos = int(lenXPos/2)
        # y calcs
        y = int((lcoord[0] + rcoord[0])/2)
        yUp = y - 50
        yDown = y + 50

        # print(f'xIniP={xIniPos}, xEndP={xEndPos}, lenXP={lenXPos}, halfX={halfXPos}')
        # print(f'y={y}, yUp={yUp}, yDown={yDown}')
        
        lPart = img[yUp:yDown, xIniPos:(halfXPos + xIniPos)]
        rPart = img[yUp:yDown, (xEndPos - halfXPos):xEndPos]

        lCross = self.findCrossCoord(lPart, True)
        # compute the right coords on the total image
        lCross[1] = xIniPos + lCross[1] 
        lCross[0] = yUp + lCross[0]

        rCross = self.findCrossCoord(rPart, False)
        # compute the right coords on the total image
        rCross[1] = xIniPos + halfXPos + rCross[1]
        rCross[0] = yUp + rCross[0]        

        return (lCross, rCross)

    def findMiddlePart(self, img, lcoord, rcoord):
        """In charge of: 
            (1) calculate the coords related with a third part from what was founded using method findDistancesCupRegion

        Keyword arguments:
        img -- An image to read
        lcoord -- points from left side of the image from cup region
        rcoord -- points from right side of the image from cup region

        Returns: 
        Will be return:
            - a coord (x, y) where is the third part
        """
        bestCoordinate = list([0, 0])
        
        lenEqualPartsX = (rcoord[1] - lcoord[1])/3
        
        x = int(lcoord[1] + lenEqualPartsX + (lenEqualPartsX/2))
        
        y = int((lcoord[0] + rcoord[0])/2)
        yUp = y - 50
        yDown = y + 50

        imgRegion = img[yUp:yDown, x:x+1]

        for pHeight in range(imgRegion.shape[0]):
            for pWidth in range(imgRegion.shape[1]):
                selectedPixel = imgRegion[pHeight, pWidth]
                if (selectedPixel[0] == 0 and
                    selectedPixel[1] == 0 and
                    selectedPixel[2] == 255):
                    print(pHeight)
                    bestCoordinate = list([pHeight + 1, pWidth])
                break
            
            if any(bestCoordinate):
                break

        print(bestCoordinate)

        bestCoordinate[0] = yUp + bestCoordinate[0]
        bestCoordinate[1] = x

        return bestCoordinate

    def findCrossCoord(self, img, reversed) -> list:
        """Search the point where cross line from 'edges' with layer1
        """
        bestCoordinate = list([0, 0])
        lWidth = []
        
        if reversed:
            lWidth = range(img.shape[1])[::-1]
        else:
            lWidth = range(img.shape[1])
        
        for pHeight in range(img.shape[0]):
            for pWidth in lWidth:
                selectedPixel = img[pHeight, pWidth]
                if (selectedPixel[0] in range(245, 255) and 
                    selectedPixel[1] in range(245, 255) and 
                    selectedPixel[2] in range(245, 255)):
                    pNext = pHeight + 1 if pHeight < 99 else pHeight
                    downPixel = img[pNext, pWidth]
                    if (downPixel[0] == 0 and
                        downPixel[1] == 0 and
                        downPixel[2] == 255):
                        print(f'pixel vermelho: pH{pNext}, pW:{pWidth}, downP:{downPixel}')
                        bestCoordinate = list([pNext, pWidth])
                    break

        return bestCoordinate

    def findCoord(self, img) -> list:
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