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

import re
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
def blacklist(comment):
    
    return True if (comment.body.lower(), comment.body)[Globals.config["caseSensitive"]] in Globals.config["blacklist"] else False


# Checks a given value against an array; the value passes the
# check either if it is in the array or if the array is empty
def checkArray(array: List, value: Any) -> bool:
    
    return True if len(array) < 1 or value in array else False


# Regex check; placed here for easy of readability in main.py.
def regex(comment):
    
    return True if Globals.config["useRegex"] and checkRegex(re, comment) else False


# The main comment deletion algorithm
def remover(comment: object) -> NoReturn:
    
    if checkArray(Globals.config["subredditList"], str(comment.subreddit).lower()) and checkArray(Globals.config["userList"], comment.parent().author.name):
        
        # Only delete comments older than the cutoff
        if time() - comment.created_utc > Globals.config["cutoffSec"]:
            Log.new([f"Obsolete '{comment.body}' found, deleting."])
            if not Globals.config["debug"]:
                comment.delete()
                Stats.increment("deleted")
        else:
            Log.new([f"Waiting for '{comment.body}'."])
            Stats.increment("waitingFor")
