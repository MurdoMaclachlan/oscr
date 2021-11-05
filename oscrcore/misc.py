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

    This module is divided into several categories, which is probably
    contradictory to its classification as "misc", but it's my module
    and I'll modulate it however I please.
"""

import json
import sys
from typing import Dict, List, NoReturn, TextIO
from .globals import Globals, Log, System
global Globals, Log, System


"""
    CONFIGURATION FUNCTIONS
    
    These functions are related to the config and praw.ini, including
    the creation, retrieval and management of these files.
"""


def checkConfig() -> NoReturn:
    """Checks if all necessary config options exist within the config file.

    No arguments.

    No return value.
    """
    from .globals import DEFAULT_CONFIG
    
    # Check to see if each key in the default config is also in the config file
    for key in DEFAULT_CONFIG:
        if key not in Globals.config:
            Log.new([Log.warning(f"Detected missing config key: {key}. Adding with default value.")])
            Globals.config[key] = DEFAULT_CONFIG[key]

    dumpConfig()


def dumpConfig() -> bool:
    """Attempts to dump the config to the config file

    No arguments.

    Returns: boolean success status.
    """
    return dumpJSON(
            f"{System.PATHS['config']}/config.json",
            {"config": [Globals.config]}
    )


def getConfig() -> NoReturn:  
    """Retrieves the config from the config.json file; if no config is found, creates
    one from the default values.

    No arguments.

    No return value.
    """
    try:
        with open(f"{System.PATHS['config']}/config.json") as configFile:
            try: data = json.load(configFile)
            
            # Catch invalid JSON in the config file (usually a result of manual editing)
            except json.decoder.JSONDecodeError as e:
                print(
                    Log.warning("Failed to get config; could not decode JSON file. Exiting."),
                    f"Error was: {e}"
                )
                sys.exit(0)
            
            Globals.config = data["config"][0]
            
            checkConfig()

    # Catch missing config file
    except FileNotFoundError:
        from .globals import DEFAULT_CONFIG
        Globals.config = DEFAULT_CONFIG
        Globals.config["user"] = input("No config file found. Please enter your Reddit username:  /u/")
        dumpConfig()


"""
    TRUE MISCELLANEOUS
    
    The following functions don't fit into any real
    category at all.
"""


def calculateEssentials() -> NoReturn:
    """Performs any necessary one-time calculations or changes relating to the config.

    No arguments.

    No return value.
    """
    # Will default any non-numeric limits to 1000.
    if not str(Globals.config["limit"]).isnumeric():
        Globals.config["limit"] = 1000

    # Attempts to calculate the cutoff time and wait time in seconds
    for keyList in [["cutoffSec", "cutoff", "cutoffUnit", 3600], ["waitTime", "wait", "unit", 1800]]:
        try:
            if type(Globals.config[keyList[2]]) == list:
                Globals.config[keyList[0]] = Globals.config[keyList[1]] * Globals.config[keyList[2]][2]
            else:
                Globals.config[keyList[0]] = Globals.config[keyList[1]] * Globals.config[keyList[2]]

        # Defaults to one hour / half an hour if any of the related variables is missing or corrupted
        except (KeyError, TypeError):
            Globals.config[keyList[0]] = keyList[3]

            
def checkRegex(re, comment: str) -> bool:
    """Checks a given string against all members of the regex blacklist.

    Arguments:
    - re (module)
    - comment (string)

    Returns: boolean.
    """
    for pattern in Globals.config["regexBlacklist"]:
        if re.match(pattern, (comment.casefold(), comment)[Globals.config["caseSensitive"]]):
            return True
    return False


def dumpJSON(path: str, data: Dict) -> bool:
    """Dumps dictionary as JSON content to a given path.

    Arguments:
    - path (string)
    - data (dictionary)

    Returns: boolean success status.
    """
    try:
        with open(path, "w") as outFile:
            outFile.write(json.dumps(data, indent=4, sort_keys=True))
        return True
    except FileNotFoundError: return False


def filterArray(array: List, elements: List) -> List:
    """Deletes a portion of a given array based on given elements.

    Arguments:
    - array (array)
    - elements (array)

    Returns: a single array.
    """
    del array[array.index(elements[0]):array.index(elements[len(elements)-1])]
    return array


def writeToFile(content: List, file: TextIO) -> bool:
    """Writes each element of a list as a new line to a given file.

    Arguments:
    - content (list)
    - file (TextIO instance)

    Returns: boolean success status.
    """
    for line in content: file.write(line+"\n")
    return True
