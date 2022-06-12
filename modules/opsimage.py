import cv2
import PIL.Image

class OpsImage():
    def __init__(self):
        pass

    def mergeImages(self, layerl1, layerl2, mergedPath):
        for idx, il1 in enumerate(layerl1):
            background = PIL.Image.open(il1)
            foreground = PIL.Image.open(layerl2[idx])
            
            background.paste(foreground, (0, 0), foreground)
            background.save(mergedPath[idx])