#!/usr/bin/env python3

# Credit to u/--B_L_A_N_K-- for improving the system and allowing it to delete in real-time, and for helping to improve console output formatting.
# Credit to u/DasherPack for being a handsome boy.

import praw
import time
import libcdr
from config import *

version = "0.4.1"

# Retieves the date the comment was posted at.
def getDate(comment):
    return comment.created_utc

reddit = praw.Reddit("credentials", user_agent=os+":claimdoneremover:v"+version+" (by u/MurdoMaclachlan)")

log = []

libcdr.doLog("Running CDRemover with recur set to {}.".format(recur), log)

# Retrieves stats
totalCounted = libcdr.fetch("counted", log)
totalDeleted = libcdr.fetch("deleted", log)


# Updates the log.
def updateLog(message, log):
    libcdr.doLog(message, log)
    if libcdr.attemptLog(log):
        del log[:]
        return log
    else:
        print("{} - Log error; disabling log updates for this instance.".format(getTime(time.time())))
        logUpdates = False
        return logUpdates

if logUpdates == True:
    log = updateLog("Updating log...", log)
    log = updateLog("Log updated successfully.", log)

while True:
    deleted = 0
    counted = 0
    waitingFor = 0

    # Checks all the user's comments, deleting them if they're past the cutoff. Exits the program if it encounters an API error.
    for comment in reddit.redditor(user).comments.new(limit=limit):
        if comment.body in blacklist:
            if time.time() - getDate(comment) > cutoff*3600:
                libcdr.doLog("Obsolete '{}' found, deleting.".format(comment.body), log)
                comment.delete()
                deleted += 1
            else:
                waitingFor += 1
        counted += 1

    # Updates statistics
    totalCounted += counted
    totalDeleted += deleted
    libcdr.update("counted", totalCounted, log)
    libcdr.update("deleted", totalDeleted, log)
    
    # Gives info about this iteration; how many comments were counted, deleted, still waiting for.
    libcdr.doLog("Counted this cycle: {}".format(str(counted)), log)
    libcdr.doLog("Deleted this cycle: {}".format(str(deleted)), log)
    libcdr.doLog("Waiting for: {}".format(str(waitingFor)), log)
    libcdr.doLog("Total Counted: {}".format(str(totalCounted)), log)
    libcdr.doLog("Total Deleted: {}".format(str(totalDeleted)), log)

    # If recur is set to false, updates log and kills the program.
    if recur == False:
        log = updateLog("Updating log...", log)
        log = updateLog("Log updated successfully.", log)
        updateLog("Exiting...", log)
        break

    # Updates log, prepares for next cycle.
    if logUpdates == True:
        log = updateLog("Updating log...", log)
        log = updateLog("Log updated successfully.", log)
        libcdr.doLog("Waiting {} {} before checking again...".format(str(wait), unit[0] if wait == 1 else unit[1]), log)
        log = updateLog("", log)
    else:
        libcdr.doLog("Waiting {} {} before checking again...".format(str(wait), unit[0] if wait == 1 else unit[1]), log)

    time.sleep(wait*unit[2])
