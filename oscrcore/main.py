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

import signal
from time import sleep
from typing import Any
from .auth import init
from .classes import Globals, Stats
from .comment import check_comments
from .log import exit_with_log, update_log
from .logger import Log
from .statistics import update_and_log_stats


def oscr() -> None:
    """The primary OSCR function controlling the flow of all primary functionality. Also
    a hot mess.

    No arguments.

    No return value.
    """
    signal.signal(signal.SIGINT, signal_handler)
    Log.new(
        f"Running OSCR version {Globals.VERSION} with recur set to"
        + f" {Globals.get(key='recur')}.",
        "INFO"
    ),
    if not Globals.get(key="log_updates"):
        Log.new(
            "Log updates are OFF. Console log will not be saved for this instance.",
            "WARNING"
        )

    # Initialises Reddit instance
    reddit = init()

    # Fetches statistics
    if Globals.get(key="report_totals"):
        from .statistics import fetch_stats
        fetch_stats()
    (
        update_log(["Updating log...", "Log updated successfully."])
        if Globals.get(key="log_updates")
        else None
    )

    while True:

        Stats.reset()

        # Fetches the comment list from Reddit
        Log.new("Retrieving comments...", "INFO")
        profile = reddit.redditor(Globals.get(key="user"))
        comment_list = profile.comments.new(limit=Globals.get(key="limit"))
        Log.new("Comments retrieved; checking...", "INFO")

        # Iterate through commentList and delete any that meet requirements
        check_comments(comment_list)

        Log.new(
            f"Successfully checked all {Stats.get('current', stat='counted')}"
            + " available comments.",
            "INFO"
        )

        # Notifies if the end of Reddit's listing is reached (i.e. no new comments due
        # to API limitations)
        if Stats.get("current", stat="counted") < Globals.get(key="limit"):
            Log.new(
                "OSCR counted less comments than your limit of"
                + f" {Globals.get(key='limit')}. You may have deleted all"
                + " available eligible comments, or a caching error may have"
                + " caused Reddit to return less comments than it should. It may"
                + " be worth running OSCR once more.",
                "WARNING"
            )

        update_and_log_stats()

        # If recur is set to false, updates log and kills the program.
        if not Globals.get(key="recur"):
            exit_with_log(["Updating log...", "Log updated successfully."])

        # Updates log, prepares for next cycle.
        update_log(
            [
                "Updating log...",
                "Log updated successfully.",
                f"Waiting {str(Globals.get(key='wait'))} "
                + str(
                    Globals.get(key='unit')[0] if Globals.get(key='wait') == 1
                    else Globals.get(key='unit')[1]
                )
                + " before checking again..."
            ]
        )
        sleep(Globals.get(key="wait_time"))


def signal_handler(sig: int, frame: Any) -> None:
    """Gracefully exit; don't lose any as-yet unsaved log entries.

        :param sig: int
        :param frame: Any

        :return: Nothing.
    """
    from .statistics import dump_stats
    if not Log.bar.close():
        print("\r", end="\r")
    update_log("Received kill signal, exiting...")
    if Stats.enabled:
        Stats.update_totals()
        dump_stats()
    exit(0)
