import os
import sys
import cv2
import logging
import management
import coordinates
import opsimage

sys.path.insert(1, '../common')

import configs

def main():

    logging.basicConfig(
        filename='../log/trace.log', 
        format='%(levelname)s: %(asctime)s - %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p', 
        level=logging.INFO, 
        filemode='w'
    )
    logging.info("")
    logging.info("Starting the script...")
    
    configMap = configs.ConfigMap()

    mg = management.Management(configMap.dirs)
    mg.run()

    coords = coordinates.Coordinates(mg)    
    coords.initialCoords()
                
    opsImage = opsimage.OpsImage(mg, coords)
    opsImage.run()

    logging.info("Ended the script...")
    logging.info("")

if __name__ == "__main__":
    main()