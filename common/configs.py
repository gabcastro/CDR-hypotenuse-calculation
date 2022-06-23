import os
import logging
import configparser

class ConfigMap():
    sectionIni = "Paths"
    sectionLog = "Log"

    def __init__(self):
        self.configParser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.configParser.read("../common/configs.ini")
        self.dirs = {}

        self.configTempFolders()

        logging.info('File of configs readed')


    @property
    def dirs(self):
        return self._dirs
    @dirs.setter
    def dirs(self, d):
        self._dirs = d
        for opt in self.configParser.options(self.sectionIni):
            val = self.configParser.get(section=self.sectionIni, option=opt)
            self._dirs[opt] = val


    def configTempFolders(self):
        mergeFolder = self.dirs["dirmerged"]
        outFolder = self.dirs["dirout"]

        self.createFolder(mergeFolder)
        self.createFolder(outFolder)

    def createFolder(self, folder):
        if not (os.path.isdir(folder)):
            logging.info(f"Created folder: {folder}")
            os.mkdir(folder)