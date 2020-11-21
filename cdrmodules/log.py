import time
from os import mkdir
from os.path import isfile, isdir
from .misc import getTime
from .gvars import *

# Updates the log array and prints to console
def doLog(output):
    
    global log
    
    if not output == "":
        currentTime = getTime(time.time())
        try:
            log.append(f"{currentTime} - {output}\n")
            print(f"{currentTime} - {output}")
        except AttributeError as e:
            print(currentTime+" - "+f"Failed to update log; log is {log}.")
            print(f"Error is {e}")
            return False
    return True

# Updates the log file with the current log.
def updateLog(message, config):
    
    global log, home
    
    doLog(message)
    if attemptLog():
        del log[:]
        return config["logUpdates"]
    else:
        print(f"{getTime(time.time())} - Log error; disabling log updates for this instance.")
        logUpdates = False
        return logUpdates

# Writes the contents of the log array to the log.txt file
def writeLog():
    
    global log, home
    
    with open(home+"/.cdremover/data/log.txt", "a") as file:
        for i in log:
            file.write(i)
    return True
    
# Attempts to update log.txt file, creating any missing files/directories.
def attemptLog():
    
    global log, home
    
    try:
        writeLog()
        return True
        
    # Creates log.txt and/or the data directory, if necessary.
    except FileNotFoundError:
        doLog("No log.txt found; attempting to create.")
        if not isdir(home+"/.cdremover/data"):
            mkdir(home+"/.cdremover/data")
            writeLog()
        return True
