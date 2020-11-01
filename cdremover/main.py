#!/usr/bin/env python3

# Credit to /u/--B_L_A_N_K-- for improving the system and allowing it to delete in real-time, and for helping to improve console output formatting.
# Credit to /u/DasherPack for being a handsome boy.

import praw
import time
import sys
import configparser
from os.path import expanduser
from .__init__ import *

home = expanduser("~")

config = getConfig(home)

version = "1.0.0-pre3"

instance = False
attempts = 0
while instance == False:
    if attempts == 3:
        print("Could not find praw.ini file after 3 attempts. Exiting.")
        sys.exit(0)
    try:
        reddit = praw.Reddit("credentials", user_agent=config["os"]+":claimdoneremover:v"+version+" (by u/MurdoMaclachlan)")
        instance = True
    except configparser.NoSectionError:
        createIni()
        attemps += 1

log = []
doLog("Running CDRemover version {} with recur set to {}.".format(version, config["recur"]), log)

# Retrieves stats
totalCounted = fetch("counted", log, home)
totalDeleted = fetch("deleted", log, home)

def remover(comment, cutoff, deleted, waitingFor):
    if time.time() - getDate(comment) > cutoff*3600:
        doLog("Obsolete '{}' found, deleting.".format(comment.body), log)
        comment.delete()
        deleted += 1
    else:
        doLog("Waiting for '{}'.".format(comment.body), log)
        waitingFor += 1
    return deleted, waitingFor

if config["logUpdates"] == True:
    logUpdates, log = updateLog("Updating log...", log, config, home)
    logUpdates, log = updateLog("Log updated successfully.", log, config, home)

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
    update("counted", totalCounted, log, home)
    update("deleted", totalDeleted, log, home)
    
    # Gives info about this iteration; how many comments were counted, deleted, still waiting for.
    doLog("Counted this cycle: {}".format(str(counted)), log)
    doLog("Deleted this cycle: {}".format(str(deleted)), log)
    doLog("Waiting for: {}".format(str(waitingFor)), log)
    doLog("Total Counted: {}".format(str(totalCounted)), log)
    doLog("Total Deleted: {}".format(str(totalDeleted)), log)

    # If recur is set to false, updates log and kills the program.
    if config["recur"] == False:
        logUpdates, log = updateLog("Updating log...", log, config, home)
        logUpdates, log = updateLog("Log updated successfully.", log, config, home)
        updateLog("Exiting...", log, config, home)
        break

    # Updates log, prepares for next cycle.
    if logUpdates == True:
        logUpdates, log = updateLog("Updating log...", log, config, home)
        logUpdates, log = updateLog("Log updated successfully.", log, config, home)
        doLog("Waiting {} {} before checking again...".format(str(config["wait"]), config["unit"][0] if config["wait"] == 1 else config["unit"][1]), log)
        logUpdates, log = updateLog("", log, config, home)
    else:
        doLog("Waiting {} {} before checking again...".format(str(config["wait"]), config["unit"][0] if config["wait"] == 1 else config["unit"][1]), log)

    time.sleep(config["wait"]*config["unit"][2])
