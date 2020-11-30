import time
from os import mkdir
from os.path import isdir
from .misc import getTime

# Updates the log array and prints to console
def doLog(output, gvars):
    
    if not output == "":
        currentTime = getTime(time.time())
        try:
            gvars.log.append(f"{currentTime} - {output}\n")
            print(f"{currentTime} - {output}")
        except AttributeError as e:
            print(currentTime+" - "+f"Failed to update log; log is {gvars.log}.")
            print(f"Error is {e}")
            return False
    return True

# Updates the log file with the current log.
def updateLog(message, gvars):
    
    if gvars.config["logUpdates"]:
        doLog(message, gvars)
        if attemptLog(gvars):
            del gvars.log[:]
            return True
        else:
            print(f"{getTime(time.time())} - Log error; disabling log updates for this instance.")
            gvars.config["logUpdates"] = False
    return False

# Writes the contents of the log array to the log.txt file
def writeLog(gvars):
    
    with open(gvars.home+"/.oscr/data/log.txt", "a") as file:
        for i in gvars.log:
            file.write(i)
    return True
    
# Attempts to update log.txt file, creating any missing files/directories.
def attemptLog(gvars):
    
    try:
        writeLog(gvars)
        return True
        
    # Creates log.txt and/or the data directory, if necessary.
    except FileNotFoundError:
        doLog("No log.txt found; attempting to create.", gvars)
        if not isdir(gvars.home+"/.oscr/data"):
            mkdir(gvars.home+"/.oscr/data")
            writeLog(gvars)
        return True
