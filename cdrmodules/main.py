#!/usr/bin/env python3

# Credit to /u/--B_L_A_N_K-- for improving the system and allowing it to delete in real-time, and for helping to improve console output formatting.
# Credit to /u/DasherPack for being a handsome boy.

import praw
import time
import sys
import configparser
from .__init__ import *
from .gvars import *

# config setup and start message
config = getConfig()
doLog("Running CDRemover version {} with recur set to {}.".format(version, config["recur"]))

# Retrieves stats
totalCounted = fetch("counted")
totalDeleted = fetch("deleted")

# Initialises Reddit() instance
try:
    reddit = praw.Reddit("cdrcredentials", user_agent=config["os"]+":claimdoneremover:v"+version+" (by u/MurdoMaclachlan)")
except (configparser.NoSectionError, praw.exceptions.MissingRequiredAttributeException):
    if createIni():
        doLog("praw.ini successfully created, program restart required for this to take effect.")
        updateLog("Exiting...", config)
    else:
        doLog("Failed to create praw.ini file, something went wrong.")
        updateLog("Exiting...", config)
    sys.exit(0)

def remover(comment, cutoff, deleted, waitingFor):
    if time.time() - getDate(comment) > cutoff:
        doLog("Obsolete '{}' found, deleting.".format(comment.body))
        comment.delete()
        deleted += 1
    else:
        doLog("Waiting for '{}'.".format(comment.body))
        waitingFor += 1
    return deleted, waitingFor

if config["logUpdates"] == True:
    logUpdates = updateLog("Updating log...", config)
    logUpdates = updateLog("Log updated successfully.", config)

while True:
    deleted = 0
    counted = 0
    waitingFor = 0

    # Checks all the user's comments, deleting them if they're past the cutoff.
    for comment in reddit.redditor(config["user"]).comments.new(limit=config["limit"]):
        if config["torOnly"]:
            if comment.body.lower() in config["blacklist"] and str(comment.subreddit).lower() == "transcribersofreddit":
                deleted, waitingFor = remover(comment, config["cutoffSec"], deleted, waitingFor)
        else:
            if comment.body.lower() in config["blacklist"]:
                deleted, waitingFor = remover(comment, config["cutoffSec"], deleted, waitingFor)
        counted += 1
        if counted % 25 == 0:
            doLog("{}/{} comments checked successfuly.".format(counted, config["limit"]))

    # Updates statistics
    totalCounted += counted
    totalDeleted += deleted
    update("counted", totalCounted)
    update("deleted", totalDeleted)
    
    # Gives info about this iteration; how many comments were counted, deleted, still waiting for.
    doLog("Counted this cycle: {}".format(str(counted)))
    doLog("Deleted this cycle: {}".format(str(deleted)))
    doLog("Waiting for: {}".format(str(waitingFor)))
    doLog("Total Counted: {}".format(str(totalCounted)))
    doLog("Total Deleted: {}".format(str(totalDeleted)))

    # If recur is set to false, updates log and kills the program.
    if not config["recur"]:
        logUpdates = updateLog("Updating log...", config)
        logUpdates = updateLog("Log updated successfully.", config)
        updateLog("Exiting...", config)
        break

    # Updates log, prepares for next cycle.
    if logUpdates:
        logUpdates = updateLog("Updating log...", config)
        logUpdates = updateLog("Log updated successfully.", config)
        doLog("Waiting {} {} before checking again...".format(str(config["wait"]), config["unit"][0] if config["wait"] == 1 else config["unit"][1]))
        logUpdates = updateLog("", config)
    else:
        doLog("Waiting {} {} before checking again...".format(str(config["wait"]), config["unit"][0] if config["wait"] == 1 else config["unit"][1]))

    time.sleep(config["waitTime"])
