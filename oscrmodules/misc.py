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

import datetime
import json
import sys
from os import environ, mkdir
from os.path import isdir

"""
    This module is divided into several categories,
    which to be fair ruins the 'misc'-ness of it, but
    you just shush there, meta. This is my module
    and I'll modulate it how I want to.
    
    getTime and the doLog import need to be here to
    avoid a circular import and now my nicely organised
    module is shite. I hate everything.
"""
   
# Finds the current time and returns it in a human readable format.
def getTime(timeToFind):
    currentTime = datetime.datetime.fromtimestamp(timeToFind)
    return currentTime.strftime("%Y-%m-%d %H:%M:%S") 

"""
    CONFIGURATION FUNCTIONS
    
    These functions are related to the config and praw.ini, including
    the creation, retrieval and management of these files.
"""

# Write to config.json
def dumpConfig(outConfig, gvars):
    
    with open(gvars.savePath+"/oscr/config.json", "w") as outFile:
        outFile.write(json.dumps(outConfig, indent=4, sort_keys=True))
    return True

# Retrieves the user configurations from a .json file, or creates a config file from default values if one can't be found.
def getConfig(gvars):

    from .log import doLog    

    try:
        with open(gvars.savePath+"/oscr/config.json") as configFile:
            try:
                fromConfig = json.load(configFile)
            
            # Catch invalid JSON in the config file (usually a result of manual editing)
            except json.decoder.JSONDecodeError as e:
                doLog([warn("Failed to get config; could not decode JSON file. Exiting.", gvars), f"Error was: {e}"], gvars)
                sys.exit(0)
            
            gvars.config = fromConfig["config"][0]

    # Catch missing config file
    except FileNotFoundError:
        from .gvars import defaultConfig
        gvars.config = defaultConfig
        gvars.config["user"] = input("No config file found. Please enter your Reddit username:  /u/")
        tryDumpConfig(gvars)

    return gvars

# Attempts to update the config file
def tryDumpConfig(gvars):
    
    from .log import doLog
    
    outConfig = {"config": [gvars.config]}
    
    try:
        return dumpConfig(outConfig, gvars)
    
    # Catch missing config directory for OSCR
    except FileNotFoundError:
        doLog(["home/.config/oscr directory not found; creating."], gvars)
        if not isdir(gvars.home+"/.config/oscr"):
            mkdir(gvars.home+"/.config/oscr")
            return dumpConfig(outConfig, gvars)
        
        # I don't think this will ever be reached, but it's here just in case
        else:
            return doLog(["What the hell happened here?"], gvars)

"""
    TRUE MISCELLANEOUS
    
    The following functions don't fit into any real
    category at all.
"""

# Performs any necessary one-time calculations and changes relating to the config
def calculateEssentials(gvars):
    
    # Will default any non-numeric limits, or a limit of 1000, to None.
    if not str(gvars.config["limit"]).isnumeric() or gvars.config["limit"] >= 1000:
        gvars.config["limit"] = None
    
    # Attempts to calculate the cutoff time and wait time in seconds
    for keyList in [["cutoffSec", "cutoff", "cutoffUnit", 3600], ["waitTime", "wait", "unit", 1800]]:
        try:
            if type(gvars.config[keyList[2]]) is list:
                gvars.config[keyList[0]] = gvars.config[keyList[1]]*gvars.config[keyList[2]][2]
            else:
                gvars.config[keyList[0]] = gvars.config[keyList[1]]*gvars.config[keyList[2]]
        
        # Defaults to one hour / half an hour if any of the related variables is missing or corrupted
        except (KeyError, TypeError):
            gvars.config[keyList[0]] = keyList[3]
    
    return gvars

def checkRegex(gvars, re, comment):
    return True if sum([True for pattern in gvars.config["regexBlacklist"] if re.match(pattern, (comment.body.lower(), comment.body)[gvars.config["caseSensitive"]])]) > 0 else False

# Finds the correct save path for config files, based on OS
def defineSavePath(home):
    
    if sys.platform.startswith("win"): return home + environ["APPDATA"]
    else: return home + "/.config"

def filterArray(array, elements):
    start = array.index(elements[0])
    end = array.index(elements[len(elements)-1])
    del array[start:end]
    return array

def writeToFile(gvars, content, file):
    for line in content:     
        file.write(line+"\n")
    return True
