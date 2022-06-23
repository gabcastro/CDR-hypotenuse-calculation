import os
import cv2
import logging
import PIL.Image
import management
import coordinates

class OpsImage():

    def __init__(self, objMg, objCoord):
        self.mg = objMg
        self.coord = objCoord

    def run(self):
        self.mergeImages()
        self.ops(self.coord.allLCoords, self.coord.allRCoords, self.coord.allInnerCoords)

    def mergeImages(self):
        """Merge the layer 1 and 2 in an unique img and save in a folder
        """
        listL1 = self.mg.fullPathImgs[0]
        listL2 = self.mg.fullPathImgs[1]

        for idx, il1 in enumerate(listL1):
            try:
                background = PIL.Image.open(il1)
                foreground = PIL.Image.open(listL2[idx])
            
                background.paste(foreground, (0, 0), foreground)
                background.save(self.mg.fullPathMerged[idx])
            except:
                logging.error("Something went wrong when trying merge L1 with L2")

        logging.info("L1 - L2 merged and saved at MERGED folder")

    def ops(self, lCoords : list, rCoords : list, innerCoords: list):
        """For all images, will:
            (1) read all left and right points, to compute limits and third part
            (2) merge found value to third part with inner coord
        """
        for idx, img in enumerate(self.mg.fullPathMerged):
            logging.info(img)
            actImg = cv2.imread(img)

            i = self.drawLine(actImg, lCoords[idx], rCoords[idx], (0, 0, 255))

            (lCross, rCross) = self.coord.findDistancesCupRegion(i, lCoords[idx], rCoords[idx])
            logging.info(f"\t\t* found coords (cup region)")

            i = self.drawDot(i, (lCross[1], lCross[0]), 5, (0, 200, 0))
            i = self.drawDot(i, (rCross[1], rCross[0]), 5, (0, 200, 0))

            thirdPart = self.coord.findMiddlePart(i, lCross, rCross)
            logging.info(f"\t\t* found coords (center of third part)")

            i = self.drawDot(i, (thirdPart[1], thirdPart[0]), 5, (230, 0, 0))

            i = self.drawLine(i, thirdPart, innerCoords[idx], (230, 0, 0))

            self.coord.adjacentSide(thirdPart, innerCoords[idx])
            self.coord.opositeSide(thirdPart, lCross, rCross)
            logging.info(f"\t\t* compute values to adjacent and oposite sides")

            self.saveFinalImage(i, img)
            
            # cv2.imshow('', i)
            # cv2.waitKey(0)

    def saveFinalImage(self, img, dirImg):
        try:
            outPath = dirImg.replace("MERGED", "OUT")
            cv2.imwrite(outPath, img)
        except:
            logging.error("Something went wrong when trying save image")

    def drawLine(self, img, start_point, end_point, color):
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