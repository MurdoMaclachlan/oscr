"""
    Copyright (C) 2020-present, Murdo B. Maclachlan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
    
    Contact me at murdo@maclachlans.org.uk
"""

# Credit to /u/--B_L_A_N_K-- for improving the system and allowing it to delete in real-time, and for helping to improve console output formatting.
# Credit to /u/DasherPack for being a handsome boy.

import praw
import time
import sys
import configparser
from os import remove, rename
from .gvars import initialiseGlobals, version
from .__init__ import *

global gvars, version
gvars = initialiseGlobals(version)

if "--format-cdr" in sys.argv:
    doLog("Reformatting CDRemover files to OSCR.", gvars)
    try:
        rename(gvars.home+"/.cdremover", gvars.home+"/.oscr")
    except FileNotFoundError:
        pass
    reformatIni(gvars)
    doLog("Reformatting complete.", gvars)
if "--reset-config" in sys.argv:
    doLog("Resetting config file.", gvars)
    try:
        remove(gvars.home+"/.oscr/config.json")
    except FileNotFoundError:
        doLog("Config file already absent.", gvars)

# config setup and start message
gvars.config = getConfig(gvars)

if "--settings" in sys.argv:
    from .settings import *
    doLog(f"Running OSCR version {version} with --settings parameter, entering settings menu.", gvars)
    settingsMain(gvars)
if "--no-recur" in sys.argv:
    gvars.config["recur"] = False

doLog(f"Running OSCR version {version} with recur set to {gvars.config['recur']}.", gvars)

# Initialises Reddit() instance
try:
    reddit = praw.Reddit("oscr", user_agent=gvars.config["os"]+":oscr:v"+version+" (by /u/MurdoMaclachlan)")
except (configparser.NoSectionError, praw.exceptions.MissingRequiredAttributeException):
    if createIni(gvars):
        doLog("praw.ini successfully created, program restart required for this to take effect.", gvars)
        if not updateLog("Exiting...", gvars):
            print("Exiting...")
    else:
        doLog("Failed to create praw.ini file, something went wrong.", gvars)
        if not updateLog("Exiting...", gvars):
            print("Exiting...")
    sys.exit(0)

def remover(comment, cutoff, deleted, waitingFor):
    if time.time() - getDate(comment) > cutoff:
        doLog(f"Obsolete '{comment.body}' found, deleting.", gvars)
        comment.delete()
        deleted += 1
    else:
        doLog(f"Waiting for '{comment.body}'.", gvars)
        waitingFor += 1
    return deleted, waitingFor

# Fetches statistics
totalCounted = fetch("counted", gvars)
totalDeleted = fetch("deleted", gvars)

updateLog("Updating log...", gvars)
updateLog("Log updated successfully.", gvars)

while True:
    deleted, counted, waitingFor = 0, 0, 0

    # Checks all the user's comments, deleting them if they're past the cutoff.
    for comment in reddit.redditor(gvars.config["user"]).comments.new(limit=gvars.config["limit"]):
        if comment.body.lower() in gvars.config["blacklist"] and str(comment.subreddit).lower() in gvars.config["subredditList"]:
            deleted, waitingFor = remover(comment, gvars.config["cutoffSec"], deleted, waitingFor)
        counted += 1
        
        # Prints success check every 25 comments, or once the limit has been reached.
        if counted % 25 == 0 or counted in [1000, gvars.config["limit"]]:
            doLog(f"{counted}/{1000 if gvars.config['limit'] == None else gvars.config['limit']} comments checked successfully.", gvars)

    # Notifies if the end of Reddit's listing is reached (i.e. no new comments due to API limitations)
    try:
        if counted < gvars.config["limit"]:
            doLog(f"The end of the listing has been reached after {counted} comments; you have deleted all elligible comments.", gvars)
    except TypeError:
        doLog(f"The end of the listing has been reached after {counted} comments; you have deleted all elligible comments.", gvars)


    # Updates statistics
    totalCounted += counted
    totalDeleted += deleted
    update("counted", totalCounted, gvars)
    update("deleted", totalDeleted, gvars)
    
    # Gives info about this iteration; how many comments were counted, deleted, still waiting for.
    doLog(f"Counted this cycle: {str(counted)}", gvars)
    doLog(f"Deleted this cycle: {str(deleted)}", gvars)
    doLog(f"Waiting for: {str(waitingFor)}", gvars)
    doLog(f"Total Counted: {str(totalCounted)}", gvars)
    doLog(f"Total Deleted: {str(totalDeleted)}", gvars)

    # If recur is set to false, updates log and kills the program.
    if not gvars.config["recur"]:
        updateLog("Updating log...", gvars)
        updateLog("Log updated successfully.", gvars)
        updateLog("Exiting...", gvars)
        break

    # Updates log, prepares for next cycle.
    updateLog("Updating log...", gvars)
    updateLog("Log updated successfully.", gvars)
    doLog(f"Waiting {str(gvars.config['wait'])} {gvars.config['unit'][0] if gvars.config['wait'] == 1 else gvars.config['unit'][1]} before checking again...", gvars)
    updateLog("", gvars)

    time.sleep(gvars.config["waitTime"])
