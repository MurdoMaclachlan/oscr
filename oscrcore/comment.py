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

    This module handles methods related to working with
    the comments retrieved from Reddit.
"""

import re
from time import time
from typing import Any, List
from .classes import Globals, Log, Stats
from .misc import check_regex

global Globals, Log, Stats


def blacklist(string: str) -> bool:
    """Matches a given string value to elements of the blacklist.

    Arguments:
    - string (string)

    Returns: boolean
    """
    return (
        True
        if (string.casefold(), string)[Globals.get(key="case_sensitive")]
        in Globals.get(key="blacklist")
        else False
    )


def check_comments(comment_list: List[object]) -> None:
    """Iterates through a list of Reddit comments, deleting any that meet the
    requirements to do so.

    Arguments:
    - comment_list (a praw.models.Comment array)

    No return value.
    """
    Log.init_bar(Globals.get(key="limit"))
    # Checks all the user's comments, deleting them if they're past the cutoff.
    for comment in comment_list:
        # Reduce API calls per iteration
        body = comment.body
        try:
            if (blacklist(body), regex(body))[Globals.get(key="use_regex")]:
                remover(comment, body)
        # Result of a comment being in reply to a deleted/removed submission
        except AttributeError as e:
            Log.new(
                [
                    Log.warning(
                        "Handled error on iteration"
                        + f"{Stats.get('current', 'counted')}: {e} | Comment at"
                        + f"{comment.permalink}"
                    )
                ]
            )
        Stats.increment("counted")
        Log.bar.increment()
    Log.bar.close()


def check_array(array: List, value: Any = "", mode: str = "len") -> bool:
    """Checks a given value against an array; the value passes the check either if it is
    in the array or if the array is empty

    Arguments:
    - array (array)
    - value (any, optional, default: empty string)
    - mode (string, optional, default: "len")

    Returns: boolean.
    """
    if mode not in ["len", "val"]:
        Log.new(
            Log.warning("WARNING: unknown mode passed to check_array(). Skipping.")
        )
        return False
    return (
        True
        if (len(array) < 1 and mode == "len") or (value in array and mode == "val")
        else False
    )


def regex(string: str) -> bool:
    """Matches a given string value to regexes in the regex list.

    Arguments:
    - string (string)

    Returns: boolean.
    """
    return True if Globals.get(key="use_regex") and check_regex(re, string) else False


def remover(comment: object, body: str) -> None:
    """Main comment remover algorithm; checks that comment passes deletion requirements,
    deletes if so, counts as "waiting for" if not.

    Arguments:
    - comment (praw.Reddit.Comment instance)

    No return value.
    """
    if (
        check_array(Globals.get(key="subreddit_list"))
        and check_array(Globals.get(key="user_list"))
        or (
            (
                check_array(
                    Globals.get(key="subreddit_list"),
                    value=str(comment.subreddit).casefold(),
                    mode="val",
                )
            )
            and (
                check_array(
                    Globals.get(key="user_list"),
                    value=comment.parent().author.name,
                    mode="val",
                )
            )
        )
    ):
        # Only delete comments older than the cutoff
        if time() - comment.created_utc > Globals.get(key="cutoff_sec"):
            Log.new(f"Obsolete '{body}' found, deleting.")
            if not Globals.get(key="debug"):
                comment.delete()
                Stats.increment("deleted")
        else:
            Log.new(f"Waiting for '{body}'.")
            Stats.increment("waiting_for")