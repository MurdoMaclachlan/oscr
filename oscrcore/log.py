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

import sys
from typing import List, NoReturn
from .globals import Globals, Log, System
global Globals, Log, System

"""
    This module contains functions relating to the handling
    of log output to a file within OSCR.
    
    As with all other modules, the functions are listed in
    alphabetical order.
"""


# Exits OSCR while updating the log with some last messages
def exitWithLog(messages: List) -> NoReturn:
    
    Log.new(messages)
    
    updateLog(["Exiting..."]) if Globals.config["logUpdates"] else print("Exiting...")
        
    sys.exit(0)


# Updates the log file with the current log.
def updateLog(messages: List) -> bool:
    
    # This check is necessary to avoid empty lines in log.txt and the console output,
    # as in some places in the program, updateLog() is called with an empty array to
    # prompt the program to update the file without adding any new lines.
    if messages: Log.new(messages)
        
    if Globals.config["logUpdates"]:
        
        if writeLog():
            Log.request(["clear", "all"])
            return True
        
        else:
            print(
                Log.warning("WARNING: Error updating log; disabling log updates for this instance."),
                Log.warning("Most recent log was:\n"),
                Log.request(["get", "recent"])
            )
            Globals.config["logUpdates"] = False
    
    return False


# Writes the contents of the log array to the log.txt file
def writeLog() -> bool:
    
    try:
        with open(f"{System.PATHS['data']}/log.txt", "a") as file:
            for i in Log.request(["get", "all"]): file.write(i)
        return True
    
    # Catch all exceptions to avoid the program crashing;
    # updateLog will disable further log updates if it receives False.
    except Exception as e: print(e); return False
