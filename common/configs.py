import configparser

class ConfigMap():
    sectionIni = "Paths"

    def __init__(self):
        self.configParser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.configParser.read("../common/configs.ini")
        self.dirs = {}

    @property
    def dirs(self):
        return self._dirs
    @dirs.setter
    def dirs(self, d):
        self._dirs = d
        for opt in self.configParser.options(self.sectionIni):
            val = self.configParser.get(section=self.sectionIni, option=opt)
            self._dirs[opt] = val