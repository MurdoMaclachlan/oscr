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

import time
import sys
from os import mkdir
from os.path import isdir
from .misc import getTime

"""
    This module contains functions relating to the handling
    of log output within OSCR, from printing to console to
    saving that output to a .txt file in ~/.oscr/data.
    
    As with all other modules, the functions are listed in
    alphabetical order.
"""

# Attempts to update log.txt, creating any missing files/directories.
def attemptLog(gvars):
    
    try: return writeLog(gvars)
        
    # Creates log.txt and/or the data directory, if necessary.
    except FileNotFoundError:
        doLog("No log.txt found; attempting to create.", gvars)
        if not isdir(gvars.home+"/.oscr/data"):
            mkdir(gvars.home+"/.oscr/data")
        return writeLog(gvars)

# Updates the log array and prints to console
def doLog(messages, gvars):
    
    for message in messages:
        currentTime = getTime(time.time())
        
        try:
            gvars.log.append(f"{currentTime} - {message}\n")
            print(f"{currentTime} - {message}") if gvars.config["printLogs"] else None
        except AttributeError as e:
            print(warn(f"{currentTime} - Failed to output log; log is {gvars.log}."), gvars)
            print(warn(f"Error is: {e}"), gvars)
            return False
    
    return True

# Exits OSCR while updating the log with some last messages
def exitWithLog(messages, gvars):
    from .log import doLog, updateLog
    doLog(messages, gvars)
    if not gvars.config["logUpdates"] or not updateLog(["Exiting..."], gvars):
        print("Exiting...")
    sys.exit(0)

# Updates the log file with the current log.
def updateLog(messages, gvars):
    
    # This check is necessary to avoid empty lines in log.txt and the console output,
    # as in some places in the program, updateLog() is called with an empty array to
    # prompt the program to update the file without adding any new lines.
    if messages: doLog(messages, gvars)
        
    if gvars.config["logUpdates"]:
        if attemptLog(gvars):
            del gvars.log[:]
            return True
        else:
            print(warn(f"{getTime(time.time())} - Log error; disabling log updates for this instance."), gvars)
            gvars.config["logUpdates"] = False
    
    return False

# Colours warnings orange so that they stand out
def warn(message, gvars):
    return gvars.ConsoleColours.warning + message + gvars.ConsoleColours.reset

# Writes the contents of the log array to the log.txt file
def writeLog(gvars):
    
    try:
        with open(gvars.home+"/.oscr/data/log.txt", "a") as file:
            for i in gvars.log:
                file.write(i)
        return True
    
    # Catch all exceptions to avoid the program crashing;
    # updateLog will disable further log updates if it receives False.
    except Exception: return False
