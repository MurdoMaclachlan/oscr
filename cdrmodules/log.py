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

# Updates the log file with the current log.
def updateLog(message, log, config, home):
    doLog(message, log)
    if attemptLog(log, home):
        del log[:]
        return config["logUpdates"], log
    else:
        print("{} - Log error; disabling log updates for this instance.".format(getTime(time.time())))
        logUpdates = False
        return logUpdates, log

# Writes the contents of the log array to the log.txt file
def writeLog(log, home):
    with open(home+"/.cdremover/data/log.txt", "a") as file:
        for i in log:
            file.write(i)
    return True
    
# Attempts to update log.txt file, creating any missing files/directories.
def attemptLog(log, home):
    try:
        writeLog(log, home)
        return True
        
    # Creates log.txt and/or the data directory, if necessary.
    except FileNotFoundError:
        doLog("No log.txt found; creating.", log)
        if not isdir(home+"/.cdremover/data"):
            if not isdir(home+"/.cdremover"):
                os.mkdir(home+"/.cdremover")
            os.mkdir(home+"/.cdremover/data")
            writeLog(log, home)
        if not isfile(home+"/.cdremover/data/logs.txt"):
            writeLog(log, home)
        return True
