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

import json
import sys
from datetime import datetime
from os import environ, mkdir
from os.path import isdir
from typing import Dict, List, TextIO

"""
    This module is divided into several categories,
    which to be fair ruins the 'misc'-ness of it, but
    you just shush there, meta. This is my module
    and I'll modulate it how I want to.
    
    getTime needs to be here to avoid a circular
    import and now my nicely organised module is shite.
    I hate everything.
"""
   
# Finds the current time and returns it in a human readable format.
def getTime(timeToFind: int) -> str:
    return datetime.fromtimestamp(timeToFind).strftime("%Y-%m-%d %H:%M:%S")

"""
    CONFIGURATION FUNCTIONS
    
    These functions are related to the config and praw.ini, including
    the creation, retrieval and management of these files.
"""

# Write to config.json
def dumpConfig(outConfig: Dict, Globals: object) -> bool:
    
    with open(Globals.SAVE_PATH+"/oscr/config.json", "w") as outFile:
        outFile.write(json.dumps(outConfig, indent=4, sort_keys=True))
    return True

# Retrieves the user configurations from a .json file, or creates a config file from default values if one can't be found.
def getConfig(Globals: object) -> object:

    from .log import doLog    

    try:
        with open(Globals.SAVE_PATH+"/oscr/config.json") as configFile:
            try: fromConfig = json.load(configFile)
            
            # Catch invalid JSON in the config file (usually a result of manual editing)
            except json.decoder.JSONDecodeError as e:
                doLog([warn("Failed to get config; could not decode JSON file. Exiting.", Globals), f"Error was: {e}"], Globals)
                sys.exit(0)
            
            Globals.config = fromConfig["config"][0]

    # Catch missing config file
    except FileNotFoundError:
        from .globals import defaultConfig
        Globals.config = defaultConfig
        Globals.config["user"] = input("No config file found. Please enter your Reddit username:  /u/")
        tryDumpConfig(Globals)

    return Globals

# Attempts to update the config file
def tryDumpConfig(Globals: object) -> bool:
    
    from .log import doLog
    
    outConfig = {"config": [Globals.config]}
    
    try: return dumpConfig(outConfig, Globals)
    
    # Catch missing config directory for OSCR
    except FileNotFoundError:
        doLog(["home/.config/oscr directory not found; creating."], Globals)
        if not isdir(Globals.HOME+"/.config/oscr"):
            mkdir(Globals.HOME+"/.config/oscr")
            return dumpConfig(outConfig, Globals)
        
        # I don't think this will ever be reached, but it's here just in case
        else:
            doLog(["What the hell happened here?"], Globals)
            return False

"""
    TRUE MISCELLANEOUS
    
    The following functions don't fit into any real
    category at all.
"""

# Performs any necessary one-time calculations and changes relating to the config
def calculateEssentials(Globals: object) -> object:
    
    # Will default any non-numeric limits, or a limit of 1000, to None.
    if not str(Globals.config["limit"]).isnumeric() or Globals.config["limit"] >= 1000:
        Globals.config["limit"] = None
    
    # Attempts to calculate the cutoff time and wait time in seconds
    for keyList in [["cutoffSec", "cutoff", "cutoffUnit", 3600], ["waitTime", "wait", "unit", 1800]]:
        try:
            if type(Globals.config[keyList[2]]) is list:
                Globals.config[keyList[0]] = Globals.config[keyList[1]]*Globals.config[keyList[2]][2]
            else:
                Globals.config[keyList[0]] = Globals.config[keyList[1]]*Globals.config[keyList[2]]
        
        # Defaults to one hour / half an hour if any of the related variables is missing or corrupted
        except (KeyError, TypeError):
            Globals.config[keyList[0]] = keyList[3]
    
    return Globals

def checkRegex(Globals: object, re, comment: object) -> bool:
    return True if sum([True for pattern in Globals.config["regexBlacklist"] if re.match(pattern, (comment.body.lower(), comment.body)[Globals.config["caseSensitive"]])]) > 0 else False

# Finds the correct save path for config files, based on OS
def defineSavePath(home: str) -> str:
    if sys.platform.startswith("win"): return environ["APPDATA"] + "\\oscr"
    else: return home + "/.config"

def filterArray(array: List, elements: List) -> List:
    del array[array.index(elements[0]):array.index(elements[len(elements)-1])]
    return array

def writeToFile(Globals: object, content: List, file: TextIO) -> bool:
    for line in content: file.write(line+"\n")
    return True
