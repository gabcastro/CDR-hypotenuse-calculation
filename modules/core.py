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
    tempDir = configMap.dirs["dirtemp"]
    
    mg = management.Management(
        layerDir=layerDir, 
        mergeDir=mergedDir,
        tempDir=tempDir)
    mg.run()

    allInnerCoords = []
    allLCoords = []
    allRCoords = []
    coords = coordinates.Coordinates()    

    opsImage = opsimage.OpsImage(
        layerl1=mg.fullPathImgsL1, 
        layerl2=mg.fullPathImgsL2, 
        mergedPath=mg.fullPathMerged,
        dirTemp=tempDir)

    opsImage.mergeImages()

    for idx, packImgs in enumerate(mg.fullPathImgs):
        for imgActLayer in packImgs:
            actImg = cv2.imread(imgActLayer)
            grayImg = cv2.cvtColor(actImg, cv2.COLOR_BGR2GRAY)
            
            if (idx == 0):
                coords.findInnerPoint(grayImg)
                allInnerCoords.append(coords.deeperCoord)
            else:
                coords.findEdgePoint(grayImg)
                allLCoords.append(coords.leftEdgeCoord)
                allRCoords.append(coords.rightEdgeCoord)
                
    opsImage.addEdgePoints(allLCoords, allRCoords)


if __name__ == "__main__":
    main()