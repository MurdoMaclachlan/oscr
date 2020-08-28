import os
from os.path import isfile, isdir
import time
from .misc import getTime

# Updates the log array and prints to console
def doLog(output, log):
    if not output == "":
        currentTime = getTime(time.time())
        try:
            log.append("{} - {}\n".format(currentTime, output))
            print("{} - {}".format(currentTime, output))
        except AttributeError:
            print(currentTime+" - "+"Failed to update log; log is {}.".format(log))
            return False
    return True

# Writes the contents of the log array to the log.txt file
def writeLog(log):
    with open("data/log.txt", "a") as file:
        for i in log:
            file.write(i)
    return True
    
# Attempts to update log.txt file, creating any missing files/directories.
def attemptLog(log):
    try:
        writeLog(log)
        return True
        
    # Creates log.txt and/or the data directory, if necessary.
    except FileNotFoundError:
        doLog("No log.txt found; creating.", log)
        if not isdir("data"):
            os.mkdir("data")
            writeLog(log)
        if not isfile("data/logs.txt"):
            writeLog(log)
        return True
