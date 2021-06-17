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

from time import time
from typing import Any, List, NoReturn, Union
from .globals import Globals, Log, Stats
global Globals, Log, Stats

"""
    This module handles methods related to working with
    the comments retrieved from Reddit.
"""

# Checks a given value against an array; the value passes the
# check either if it is in the array or if the array is empty
def checkArray(array: List, value: Any) -> bool:
    
    return True if len(array) < 1 or value in array else False

# The main comment deletion algorithm
def remover(comment: object) -> NoReturn:
    
    # Only delete comments older than the cutoff
    if time() - comment.created_utc > Globals.config["cutoffSec"]:
        Log.new([f"Obsolete '{comment.body}' found, deleting."])
        if not Globals.config["debug"]:
            comment.delete()
            Stats.increment("deleted")
    else:
        Log.new([f"Waiting for '{comment.body}'."])
        Stats.increment("waitingFor")
