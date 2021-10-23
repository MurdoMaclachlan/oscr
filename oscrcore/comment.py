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
"""

import re
from alive_progress import alive_bar as aliveBar
from time import time
from typing import Any, List, NoReturn
from .globals import Globals, Log, Stats
from .misc import checkRegex
global Globals, Log, Stats

"""
    This module handles methods related to working with
    the comments retrieved from Reddit.
"""


# Blacklist check; placed here for ease of readability in main.py.
def blacklist(string: str) -> bool:
    
    return True if (string.casefold(), string)[Globals.config["caseSensitive"]] in Globals.config["blacklist"] else False


def checkComments(commentList: List[object]) -> NoReturn:

    with aliveBar(Globals.config["limit"], spinner='classic', bar='classic', enrich_print=False) as progress:

        # Checks all the user's comments, deleting them if they're past the cutoff.
        for comment in commentList:

            # Reduce API calls per iteration
            body = comment.body
            try:
                if (blacklist(body), regex(body))[Globals.config["useRegex"]]:
                    remover(comment, body)

            # Result of a comment being in reply to a deleted/removed submission
            except AttributeError as e:
                Log.new([Log.warning(f"Handled error on iteration {Stats.get('counted')}: {e} | Comment at {comment.permalink}")])

            Stats.increment("counted")
            progress()


# Checks a given value against an array; the value passes the
# check either if it is in the array or if the array is empty
def checkArray(array: List, value: Any = "", mode: str = "len") -> bool:
    
    if mode not in ["len", "val"]:
        Log.new([Log.warning("WARNING: unknown mode passed to checkArray(). Skipping.")])
        return False
    return True if (len(array) < 1 and mode == "len") or (value in array and mode == "val") else False


# Regex check; placed here for easy of readability in main.py.
def regex(string: str) -> bool:
    
    return True if Globals.config["useRegex"] and checkRegex(re, string) else False


# The main comment deletion algorithm
def remover(comment: object, body: str) -> NoReturn:
    
    if (
        checkArray(Globals.config["subredditList"]) and checkArray(Globals.config["userList"]) or
        (
            checkArray(Globals.config["subredditList"], value=str(comment.subreddit).casefold(), mode="val") and
            checkArray(Globals.config["userList"], value=comment.parent().author.name, mode="val")
        )):

            # Only delete comments older than the cutoff
            if time() - comment.created_utc > Globals.config["cutoffSec"]:
                Log.new([f"Obsolete '{body}' found, deleting."])
                if not Globals.config["debug"]:
                    comment.delete()
                    Stats.increment("deleted")
            else:
                Log.new([f"Waiting for '{body}'."])
                Stats.increment("waitingFor")
