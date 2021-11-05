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

    Contact me at murdomaclachlan@duck.com

    ----------

    Beneath is the main program. From here, all run-time flow of the
    main OSCR program is controlled through the oscr() function.

    This function initiates after all arguments have been checked and
    global variables have been collected and processed as needed, and
    continues to loop until run-time ends.
"""

import praw
import configparser
from time import sleep
from typing import NoReturn
from .auth import init
from .globals import Globals, Log, Stats
from .comment import check_comments
from .log import exit_with_log, update_log
from .statistics import update_and_log_stats
global Globals, Log, Stats


def oscr() -> NoReturn:
    """The primary OSCR function controlling the flow of all primary functionality. Also
    a hot mess.

    No arguments.

    No return value.
    """
    Log.new([
        f"Running OSCR version {Globals.VERSION} with recur set to {Globals.config['recur']}.",
        Log.warning("WARNING: Log updates are OFF. Console log will not be saved for this instance.") if not Globals.config["logUpdates"] else ""
    ])

    # Initialises Reddit instance
    reddit = init()

    # Fetches statistics
    if Globals.config["reportTotals"]:
        from .statistics import dumpStats, fetch_stats
        fetch_stats()

    update_log(["Updating log...", "Log updated successfully."]) if Globals.config["logUpdates"] else None

    while True:

        Stats.reset()

        # Fetches the comment list from Reddit
        Log.new(["Retrieving comments..."])
        comment_list = reddit.redditor(Globals.config["user"]).comments.new(limit=Globals.config["limit"])
        Log.new(["Comments retrieved; checking..."])

        # Iterate through commentList and delete any that meet requirements
        check_comments(comment_list)

        Log.new([f"Successfully checked all {Stats.get('current', stat='counted')} available comments."])

        # Notifies if the end of Reddit's listing is reached (i.e. no new comments due to API limitations)
        if Stats.get("current", stat="counted") < Globals.config["limit"]:
            Log.new([Log.warning(
                f"WARNING: OSCR counted less comments than your limit of {Globals.config['limit']}. You may have deleted all available elligible comments," +
                " or a caching error may have caused Reddit to return less coments than it should. It may be worth running OSCR once more."
            )])

        update_and_log_stats()

        # If recur is set to false, updates log and kills the program.
        if not Globals.config["recur"]:
            exit_with_log(["Updating log...", "Log updated successfully."])

        # Updates log, prepares for next cycle.
        update_log([
            "Updating log...", "Log updated successfully.",
            f"Waiting {str(Globals.config['wait'])} {Globals.config['unit'][0] if Globals.config['wait'] == 1 else Globals.config['unit'][1]} before checking again..."
        ])

        sleep(Globals.config["waitTime"])
