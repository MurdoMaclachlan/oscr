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
from .log import doLog

"""
    This module handles methods related to working with
    the comments retrieved from Reddit.
"""

def checkArray(array, value):
    
    # The value passes either if it is in the array or if the array is empty
    if len(array) < 1: return True
    elif value in array: return True
    else: return False

def removeNonAlpha(comment):
    
    # Creates new array that includes only the alpha characters
    newArray = []
    for i in list(comment):
        if i.isalpha():
            newArray.append(i)

    return ''.join(newArray)

def remover(comment, cutoff, deleted, waitingFor, Globals):
    
    # Only delete comments older than the cutoff
    if time() - comment.created_utc > cutoff:
        doLog([f"Obsolete '{comment.body}' found, deleting."], Globals)
        comment.delete()
        deleted += 1
    else:
        doLog([f"Waiting for '{comment.body}'."], Globals)
        waitingFor += 1
    return deleted, waitingFor
