from os.path import expanduser

global version

version = "1.1.0"

class Globals():
    def __init__(self, config, failedStats, home, log, version):
        self.config = config
        self.failedStats = failedStats
        self.home = home
        self.log = log
        self.version = version

def initialiseGlobals(version):
    
    global gvars
    gvars = Globals({}, [], expanduser("~"), [], version)
    return gvars
