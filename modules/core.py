import sys
import cv2
import logging
import management
import coordinates
import opsimage

sys.path.insert(1, '../common')

import configs

def main():

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info('Starting the script...')

    configMap = configs.ConfigMap()
    
    layerDir = (configMap.dirs["dirlayer1"], configMap.dirs["dirlayer2"])
    mergedDir = configMap.dirs["dirmerged"]
    mg = management.Management(layerDir=layerDir, mergeDir=mergedDir)
    mg.run()

    allCoords = []
    coords = coordinates.Coordinates()    

    opsImage = opsimage.OpsImage()
    opsImage.mergeImages(mg.fullPathImgsL1, mg.fullPathImgsL2, mg.fullPathMerged)

    for idx, packImgs in enumerate(mg.fullPathImgs):
        for imgActLayer in packImgs:
            actImg = cv2.imread(imgActLayer)
            grayImg = cv2.cvtColor(actImg, cv2.COLOR_BGR2GRAY)

    #         if (idx == 0):
    #             coords.findInnerPoint(grayImg)
    #             allCoords.append(coords.deeperCoord)
    #         else:
    #             coords.findEdgePoint(grayImg)
    #             allCoords.append(coords.leftEdgeCoord)
    #             allCoords.append(coords.rightEdgeCoord)

if __name__ == "__main__":
    main()