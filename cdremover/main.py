#!/usr/bin/env python3

# Credit to u/--B_L_A_N_K-- for improving the system and allowing it to delete in real-time, and for helping to improve console output formatting.
# Credit to u/DasherPack for being a handsome boy.

import praw
import time
import libcdr

config = libcdr.getConfig()

version = "0.4.4"

# Retieves the date the comment was posted at.
def getDate(comment):
    return comment.created_utc

reddit = praw.Reddit("credentials", user_agent=config["os"]+":claimdoneremover:v"+version+" (by u/MurdoMaclachlan)")

log = []

libcdr.doLog("Running CDRemover with recur set to {}.".format(config["recur"]), log)

# Retrieves stats
totalCounted = libcdr.fetch("counted", log)
totalDeleted = libcdr.fetch("deleted", log)

# Updates the log.
def updateLog(message, log):
    libcdr.doLog(message, log)
    if libcdr.attemptLog(log):
        del log[:]
        return config["logUpdates"], log
    else:
        print("{} - Log error; disabling log updates for this instance.".format(libcdr.getTime(time.time())))
        logUpdates = False
        return logUpdates, log

def remover(comment, cutoff, deleted, waitingFor):
    if time.time() - getDate(comment) > cutoff*3600:
        libcdr.doLog("Obsolete '{}' found, deleting.".format(comment.body), log)
        comment.delete()
        deleted += 1
    else:
        libcdr.doLog("Waiting for '{}'.".format(comment.body), log)
        waitingFor += 1
    return deleted, waitingFor

if config["logUpdates"] == True:
    logUpdates, log = updateLog("Updating log...", log)
    logUpdates, log = updateLog("Log updated successfully.", log)

while True:
    deleted = 0
    counted = 0
    waitingFor = 0

    # Checks all the user's comments, deleting them if they're past the cutoff.
    for comment in reddit.redditor(config["user"]).comments.new(limit=config["limit"]):
        if config["torOnly"] == True:
            if comment.body.lower() in config["blacklist"] and str(comment.subreddit).lower() == "transcribersofreddit":
                deleted, waitingFor = remover(comment, config["cutoff"], deleted, waitingFor)
        else:
            if comment.body.lower() in config["blacklist"]:
                deleted, waitingFor = remover(comment, config["cutoff"], deleted, waitingFor)
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
    if config["recur"] == False:
        logUpdates, log = updateLog("Updating log...", log)
        logUpdates, log = updateLog("Log updated successfully.", log)
        updateLog("Exiting...", log)
        break

    # Updates log, prepares for next cycle.
    if logUpdates == True:
        logUpdates, log = updateLog("Updating log...", log)
        logUpdates, log = updateLog("Log updated successfully.", log)
        libcdr.doLog("Waiting {} {} before checking again...".format(str(config["wait"]), config["unit"][0] if config["wait"] == 1 else config["unit"][1]), log)
        logUpdates, log = updateLog("", log)
    else:
        libcdr.doLog("Waiting {} {} before checking again...".format(str(config["wait"]), config["unit"][0] if config["wait"] == 1 else config["unit"][1]), log)

    time.sleep(config["wait"]*config["unit"][2])
