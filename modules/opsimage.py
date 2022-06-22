import os
import cv2
import PIL.Image
import coordinates

class OpsImage():

    def __init__(self, layerl1, layerl2, mergedPath, dirTemp, objCoord : coordinates):
        """Constructor

        Keyword arguments:
        layerl1 -- a list with path/img from layer 1
        layerl2 -- a list with path/img from layer 2
        mergedPath -- a list with path/img in the folder 'merged'
        """ 
        self.layerl1 = layerl1
        self.layerl2 = layerl2
        self.mergedPath = mergedPath
        self.dirTemp = dirTemp
        self.coord = objCoord

    def mergeImages(self):
        """Merge the layer 1 and 2 in an unique img and save in a folder
        """
        for idx, il1 in enumerate(self.layerl1):
            background = PIL.Image.open(il1)
            foreground = PIL.Image.open(self.layerl2[idx])
            
            background.paste(foreground, (0, 0), foreground)
            background.save(self.mergedPath[idx])

    def addEdgePoints(self, lCoords : list, rCoords : list):
        """In charge of draw a line using "edge" coords
        """
        for idx, img in enumerate(self.mergedPath):
            actImg = cv2.imread(img)

            i = self.drawLine(actImg, lCoords[idx], rCoords[idx], (0, 0, 255))

            (lCross, rCross) = self.coord.findDistancesCupRegion(i, lCoords[idx], rCoords[idx])

            i = self.drawDot(i, (lCross[1], lCross[0]), 5, (0, 200, 0))
            i = self.drawDot(i, (rCross[1], rCross[0]), 5, (0, 200, 0))

            thirdPart = self.coord.findMiddlePart(i, lCross, rCross)

            i = self.drawDot(i, (thirdPart[1], thirdPart[0]), 5, (230, 0, 0))

            cv2.imshow('', i)
            cv2.waitKey(0)

    def drawLine(self, img, start_point, end_point, color):
        # cv2.line(image, start_point, end_point, color, thickness)
        return cv2.line(
            img,
            (start_point[1], start_point[0]), 
            (end_point[1], end_point[0]), 
            color, 
            thickness=2
        )
        
    def drawDot(self, img, centerCoordinates, radius, color):
        return cv2.circle(
            img,
            centerCoordinates,
            radius,
            color,
            -1
        )