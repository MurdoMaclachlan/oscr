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

import json
import sys
from typing import Dict, List, NoReturn, TextIO
from .globals import Globals, Log, System
global Globals, Log, System

"""
    This module is divided into several categories,
    which to be fair ruins the 'misc'-ness of it, but
    you just shush there, meta. This is my module
    and I'll modulate it how I want to.
"""
   

"""
    CONFIGURATION FUNCTIONS
    
    These functions are related to the config and praw.ini, including
    the creation, retrieval and management of these files.
"""


# Checks if all necessary config options are there
def checkConfig() -> NoReturn:
    
    from .globals import DEFAULT_CONFIG
    
    # Check to see if each key in the default config is also in the config file
    for key in DEFAULT_CONFIG:
        if key not in Globals.config:
            Log.new([Log.warning(f"Detected missing config key: {key}. Adding with default value.")])
            Globals.config[key] = DEFAULT_CONFIG[key]

    dumpConfig()


# Attempts to update the config file
def dumpConfig() -> bool:
    
    return dumpJSON(
            f"{System.PATHS['config']}/config.json",
            {"config": [Globals.config]}
    )


# Retrieves the user configurations from a .json file, or creates a config file from default values if one can't be found.
def getConfig() -> NoReturn:  

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


# Performs any necessary one-time calculations and changes relating to the config
def calculateEssentials() -> NoReturn:
    
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


# Checks a comment against the regex
def checkRegex(re, comment: object) -> bool:
    for pattern in Globals.config["regexBlacklist"]:
        if re.match(pattern, (comment.body.lower(), comment.body)[Globals.config["caseSensitive"]]):
            return True
    return False


# Dumps JSON content to a given path
def dumpJSON(path: str, data: Dict) -> bool:
    
    try:
        with open(path, "w") as outFile:
            outFile.write(json.dumps(data, indent=4, sort_keys=True))
        return True
    except FileNotFoundError: return False


# Deletes a portion of a given array, based on passed elements
def filterArray(array: List, elements: List) -> List:
    del array[array.index(elements[0]):array.index(elements[len(elements)-1])]
    return array


# Writes contents of a list to a file
def writeToFile(content: List, file: TextIO) -> bool:
    for line in content: file.write(line+"\n")
    return True
