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

    def findThirdPart(self, img, lcoord, rcoord):
        """In charge of (1) search for coords between leftEdge and rightEdge, 
        but inside of cup area, (2) search for coords relate with a third part from what was founded in (1).
        Will return a (x, y) to (1), and a (x, y) to (2).
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

        # print(f'{lPart.shape} lpart || {rPart.shape} rpart')

        self.findCrossCoord(lPart)

    def findCrossCoord(self, img):
        """Search the point where cross line from 'edges' with layer1
        """
        bestCoordinate = list([0, 0])
        
        for pHeight in range(img.shape[0]):
            for pWidth in reversed(range(img.shape[1])):
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
            
        # print(bestCoordinate)

                # previousPixel = img[pHeight-1, pWidth-1]
                # if ((selectedPixel[2] == 255) and 
                #     (previousPixel[0] in range(240, 255) and
                #      previousPixel[1] in range(240, 255) and
                #      previousPixel[2] in range(240, 255))
                # ):
                #     print(f'achou na pos. pH:{pHeight} e pW:{pWidth}')
                #     bestCoordinate = list([pHeight+1, pWidth+1])
                #     stop = 1
                # elif ((bestCoordinate[0] < pHeight) and (stop == 1)):
                #     break
                # elif ((selectedPixel[0] in range(0, 230) and
                #         selectedPixel[1] in range(0, 230) and
                #         selectedPixel[2] in range(0, 230)) and
                #     (bestCoordinate[0] < pHeight) and (stop == 1)):
                #     break
            

        # print(bestCoordinate)

        # xx = cv2.circle(img, [55, 53], 2, (0, 50, 105), 2)

        # cv2.imshow('', xx)
        # cv2.waitKey(0)

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