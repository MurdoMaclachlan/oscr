import os
from os.path import isfile, isdir

def doLog(output, log):
    log.append(output+"\n")
    print(output)
    return True

def writeLog(log):
    with open("data/log.txt", "a") as file:
        for i in log:
            file.write(i)
    return True
    
def attemptLog(log):
    try:
        writeLog(log)
    except FileNotFoundError:
        doLog("No log.txt found; creating.", log)
        if not isdir("data"):
            os.mkdir("data")
            writeLog(log)
        if not isfile("data/logs.txt"):
            writeLog(log)
