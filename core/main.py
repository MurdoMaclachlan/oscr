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
from typing import NoReturn
from .globals import Globals, Log, Stats, System
from .comment import blacklist, regex, remover
from .log import exitWithLog, updateLog
from .ini import createIni, getCredentials
from .misc import writeToFile
global Globals, Log, Stats, System

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

def oscr() -> NoReturn: 

    Log.new(
        [
            f"Running OSCR version {Globals.VERSION} with recur set to {Globals.config['recur']}.",
            Log.warning("WARNING: Log updates are OFF. Console log will not be saved for this instance.") if not Globals.config["logUpdates"] else ""
        ]
    )
    
    # Initialises Reddit() instance
    try:
        reddit = praw.Reddit(
            user_agent = f"{System.OS}:oscr:v{Globals.VERSION}(by /u/MurdoMaclachlan)",
            **getCredentials()
        )
    
    # Catch for invalid ini, will create a new one then restart the program;
    # the restart is required due to current PRAW limitations. :'(
    except (configparser.NoSectionError, praw.exceptions.MissingRequiredAttributeException, KeyError):

        exitWithLog(
            ["praw.ini successfully created, program restart required for this to take effect."]
        ) if createIni() else exitWithLog(
            [Log.warning("WARNING: Failed to create praw.ini file, something went wrong.")]
        )
    
    # Fetches statistics
    if Globals.config["reportTotals"]:
        from .statistics import dumpStats, fetchStats
        fetchStats()
    
    updateLog(["Updating log...", "Log updated successfully."]) if Globals.config["logUpdates"] else None
    
    while True:
        
        Stats.reset()
        
        # Fetches the comment list from Reddit
        Log.new(["Retrieving comments..."])
        commentList = reddit.redditor(Globals.config["user"]).comments.new(limit=Globals.config["limit"])
        Log.new(["Comments retrieved; checking..."])
        
        # Initialises the progress bar
        with aliveBar(Globals.config["limit"], spinner='classic', bar='classic', enrich_print=False) as progress:
            
            # Checks all the user's comments, deleting them if they're past the cutoff.
            for comment in commentList:
                try:
                    if (blacklist(comment), regex(comment))[Globals.config["useRegex"]]:
                        remover(comment)
                
                # Result of a comment being in reply to a deleted/removed submission
                except AttributeError as e:
                    Log.new([Log.warning(f"Handled error on iteration {Globals.Stats.get('counted')}: {e} | Comment at {comment.permalink}")])
                Stats.increment("counted")
                
                progress()
    
        Log.new([f"Successfully checked all {Stats.get('current', stat='counted')} available comments."])
    
        # Notifies if the end of Reddit's listing is reached (i.e. no new comments due to API limitations)
        try:
            if Stats.get("current", stat="counted") < Globals.config["limit"]:
                Log.new([Log.warning(
                    f"WARNING: OSCR counted less comments than your limit of {Globals.config['limit']}. You may have deleted all available elligible comments," +
                    " or a caching error may have caused Reddit to return less coments than it should. It may be worth running OSCR once more."
                )])
        except TypeError:
            if Stats.get("current", stat="counted") < 1000:
                Log.new([Log.warning(
                    "WARNING: OSCR counted less comments than your limit of 1000. You may have deleted all available elligible comments," +
                    " or a caching error may have caused Reddit to return less coments than it should. It may be worth running OSCR once more."
                )])
    
        # Updates statistics
        if Globals.config["reportTotals"]:
            Stats.updateTotals()
            dumpStats()
        
        # Gives info about this iteration; how many comments were counted, deleted, still waiting for.
        Log.new(
            [
                f"Counted this cycle: {str(Stats.get('current', stat='counted'))}",
                f"Deleted this cycle: {str(Stats.get('current', stat='deleted'))}",
                f"Waiting for: {str(Stats.get('current', stat='waitingFor'))}"
            ]
        )
        if Globals.config["reportTotals"]:
            Log.new(
                [
                    f"Total Counted: {str(Stats.get('total', stat='counted'))}",
                    f"Total Deleted: {str(Stats.get('total', stat='deleted'))}"
                ]
            )
    
        # If recur is set to false, updates log and kills the program.
        if not Globals.config["recur"]:
            exitWithLog(["Updating log...", "Log updated successfully."])
    
        # Updates log, prepares for next cycle.
        updateLog(
            [
                "Updating log...",
                "Log updated successfully.",
                f"Waiting {str(Globals.config['wait'])} {Globals.config['unit'][0] if Globals.config['wait'] == 1 else Globals.config['unit'][1]} before checking again..."
            ]
        )

        sleep(Globals.config["waitTime"])
