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

    This module contains functions relating to the handling of output
    to the log file.
"""

import sys
from typing import List, NoReturn, Union
from .classes import Globals, Log, System

global Globals, Log, System


def exit_with_log(messages: Union[List[str], str]) -> NoReturn:
    """Updates the log with final message(s) then exits OSCR.

    Arguments:
    - messages (string array)

    No return value.
    """
    Log.new(messages)
    (
        update_log(["Exiting..."])
        if Globals.get(key="log_updates")
        else print("Exiting...")
    )
    sys.exit(0)


def update_log(messages: Union[List[str], str] = None) -> bool:
    """Outputs the current log to the log file, then resets the current log. Can also
    create new logs before doing so.

    Arguments:
    - messages (string array, optional, default: None)

    Returns: boolean success status
    """
    # This check is necessary to avoid empty lines in log.txt and the console output, as
    # in some places in the program, updateLog() is called with an empty array to prompt
    # the program to update the file without adding any new lines.
    if messages:
        Log.new(messages)

    if Globals.get(key="log_updates"):

        if write_log():
            Log.request(["clear", "all"])
            return True

        else:
            print(
                Log.warning(
                    "WARNING: Error updating log; disabling log updates for"
                    + " this instance."
                ),
                Log.warning("Most recent log was:\n"),
                Log.request(["get", "recent"]),
            )
            Globals.set(False, key="log_updates")

    return False


def write_log() -> bool:
    """Writes the contents of the log to log.txt.

    No arguments.

    Returns: boolean success status.
    """
    try:
        with open(f"{System.PATHS['data']}/log.txt", "a") as file:
            for i in Log.request(["get", "all"]):
                file.write(i)
        return True

    # Catch all exceptions to avoid the program crashing; update_log will disable
    # further log updates if it receives False.
    except Exception as e:
        print(f"LOG FAILURE: {e}")
        return False
