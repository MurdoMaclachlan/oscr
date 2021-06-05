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

import praw
import configparser
from time import sleep
from alive_progress import alive_bar as aliveBar
from os.path import isfile
from .log import doLog, exitWithLog, updateLog, warn
from .comment import checkArray, removeNonAlpha, remover
from .ini import createIni, extractIniDetails, getCredentials
from .misc import writeToFile

"""
    Beneath is the main program. From here, all run-time flow
    of OSCR is controlled through the oscr() function, passed
    Globals by the oscr top-level script run through the console
    command.
    
    This function initiates after all arguments have been
    checked and global variables have been collected and
    processed as needed, and continues to loop until run-time
    ends.
"""

def oscr(Globals):

    doLog(
        [
            f"Running OSCR version {Globals.VERSION} with recur set to {Globals.config['recur']}.",
            warn("WARNING: Log updates are OFF. Console log will not be saved for this instance.", Globals) if not Globals.config["logUpdates"] else None
        ], Globals
    )
    
    # Initialises Reddit() instance
    try:
        reddit = praw.Reddit(
            user_agent = Globals.config["os"] + ":oscr:v" + Globals.VERSION + " (by /u/MurdoMaclachlan)",
            **getCredentials(Globals)
        )
    
    # Catch for invalid ini, will create a new one then restart the program;
    # the restart is required due to current PRAW limitations. :'(
    except (configparser.NoSectionError, praw.exceptions.MissingRequiredAttributeException, KeyError):
        if isfile(Globals.SAVE_PATH+"/praw.ini"):
            iniDetails = extractIniDetails(Globals)
            if iniDetails is None: pass
            else:
                writeToFile(Globals, iniDetails, open(Globals.SAVE_PATH+"/oscr/praw.ini", "w+"))
                exitWithLog(["praw.ini successfully created, program restart required for this to take effect."], Globals)

        exitWithLog(["praw.ini successfully created, program restart required for this to take effect."], Globals) if createIni(Globals) else exitWithLog([warn("WARNING: Failed to create praw.ini file, something went wrong.", Globals)], Globals)
    
    # Only import regex functions if regexes are being used
    if Globals.config["useRegex"]: import re; from .misc import checkRegex
    
    # Fetches statistics
    if Globals.config["reportTotals"]:
        from .statistics import fetch, update
        totalCounted, totalDeleted = fetch("counted", Globals), fetch("deleted", Globals)
    
    updateLog(
        [
            "Updating log...",
            "Log updated successfully."
        ], Globals
    ) if Globals.config["logUpdates"] else None
    
    while True:
        deleted, counted, waitingFor = 0, 0, 0
        
        # Fetches the comment list from Reddit
        doLog(["Retrieving comments..."], Globals)
        commentList = reddit.redditor(Globals.config["user"]).comments.new(limit=Globals.config["limit"])
        doLog(["Comments retrieved; checking..."], Globals)
        
        # Initialises the progress bar
        with aliveBar(Globals.config["limit"], spinner='classic', bar='classic', enrich_print=False) as progress:
            
            # Checks all the user's comments, deleting them if they're past the cutoff.
            for comment in commentList:
                try:
                    
                    # Regex path
                    if Globals.config["useRegex"]:
                        if checkRegex(Globals, re, comment):
                            if checkArray(Globals.config["subredditList"], str(comment.subreddit).lower()) and checkArray(Globals.config["userList"], comment.parent().author.name):
                                deleted, waitingFor = remover(comment, Globals.config["cutoffSec"], deleted, waitingFor, Globals)
                    
                    # Blacklist path
                    else:
                        if removeNonAlpha((comment.body.lower(), comment.body)[Globals.config["caseSensitive"]]) in Globals.config["blacklist"]:
                            if checkArray(Globals.config["subredditList"], str(comment.subreddit).lower()) and checkArray(Globals.config["userList"], comment.parent().author.name):
                                deleted, waitingFor = remover(comment, Globals.config["cutoffSec"], deleted, waitingFor, Globals)
                
                # Result of a comment being in reply to a deleted/removed submission
                except AttributeError as e:
                    doLog([warn(f"Handled error on iteration {counted}: {e} | Comment at {comment.permalink}", Globals)], Globals)
                counted += 1
                
                progress()
    
        doLog([f"Successfully checked all {counted} available comments."], Globals)
    
        # Notifies if the end of Reddit's listing is reached (i.e. no new comments due to API limitations)
        try:
            if counted < Globals.config["limit"]:
                doLog([warn(
                    f"WARNING: OSCR counted less comments than your limit of {Globals.config['limit']}. You may have deleted all available elligible comments,",
                    "or a caching error may have caused Reddit to return less coments than it should. It may be worth running OSCR once more.",
                    Globals
                )], Globals)
        except TypeError:
            if counted < 1000:
                doLog([warn(
                    "WARNING: OSCR counted less comments than your limit of 1000. You may have deleted all available elligible comments,",
                    "or a caching error may have caused Reddit to return less coments than it should. It may be worth running OSCR once more.",
                    Globals
                )], Globals)
    
        # Updates statistics
        if Globals.config["reportTotals"]:
            totalCounted += counted
            update("counted", totalCounted, Globals)
            totalDeleted += deleted
            update("deleted", totalDeleted, Globals)
        
        # Gives info about this iteration; how many comments were counted, deleted, still waiting for.
        doLog(
            [
                f"Counted this cycle: {str(counted)}",
                f"Deleted this cycle: {str(deleted)}",
                f"Waiting for: {str(waitingFor)}"
            ], Globals
        )
        if Globals.config["reportTotals"]:
            doLog(
                [
                    f"Total Counted: {str(totalCounted)}",
                    f"Total Deleted: {str(totalDeleted)}"
                ], Globals
            )
    
        # If recur is set to false, updates log and kills the program.
        if not Globals.config["recur"]:
            exitWithLog(
                [
                    "Updating log...",
                    "Log updated successfully."
                ], Globals
            )
    
        # Updates log, prepares for next cycle.
        updateLog(
            [
                "Updating log...",
                "Log updated successfully.",
                f"Waiting {str(Globals.config['wait'])} {Globals.config['unit'][0] if Globals.config['wait'] == 1 else Globals.config['unit'][1]} before checking again..."
            ], Globals
        )

        sleep(Globals.config["waitTime"])
