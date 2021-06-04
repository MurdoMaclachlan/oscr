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

from .log import doLog, warn

"""
    This module contains file handling for the statistics,
    deleted and counted, including a function to fetch
    the stats at the beginning of run-time, and another
    to update them after each iteration.
"""

# Retrieve statistics from stats.txt
def fetch(statistic, gvars):
    
    def checkIfEmpty(array):
        if array == []:          
            doLog(f"No stats for {statistic} found; returning 0.", gvars)
            return True
    
    result = []

    try:    
        with open(gvars.home+"/.oscr/data/stats.txt", "r") as file:
            content = file.read().splitlines()
        
    # Default stat to 0 if file not found.
    except FileNotFoundError:
        doLog(f"No stats for {statistic} found; returning 0.", gvars)
        return 0


    # Default stat to 0 if file found, but appropriate statistic not found.
    if checkIfEmpty(content): return 0
    
    for line in content:
        
        # If the value for the statistic being fetched can be found, return it.
        if line.startswith(statistic):
            doLog(f"Fetched {statistic} successfully.", gvars)
            return int(line.split(" ")[1])

    # If only stat found is not the one being searched for, return 0.
    if checkIfEmpty(result): return 0

# Updates statistics in stats.txt
def update(statistic, value, gvars):

    # Necessary check to avoid further errors if stat has previously failed to update
    if statistic in gvars.failedStats:
        doLog(f"Skipping update of following statistic: {statistic}", gvars)
        return False
 
    newLine = f"{statistic}: {str(value)}"

    try:
        with open(gvars.home+"/.oscr/data/stats.txt", "r") as file:
            content = file.read().splitlines()
    
    # If stats.txt doesn't exist, create in.
    except FileNotFoundError:
        doLog("No stats.txt found; creating.", gvars)
        content = None

    with open(gvars.home+"/.oscr/data/stats.txt", "w") as file:
        
        # If no stats found, add the stat to be updated and default other to 0.
        if content == None:
            if statistic == "counted":
                file.write(newLine+"\ndeleted: 0")
            else:
                file.write("counted: 0\n"+newLine)
            doLog(f"Updated {statistic} successfully.", gvars)
            return True

        for line in content:
            
            # If both stats found, update required stat.
            if line.startswith(statistic):
                content[content.index(line)] = newLine
                file.write('\n'.join(content))
                doLog(f"Updated {statistic} successfully.", gvars)
                return True
            
        # If only stat found is not the one being searched for, add the required stat.
        content.append(newLine)
        file.seek(0)
        file.write('\n'.join(content))
        doLog(f"Updated {statistic} successfully.", gvars)
        return True
    
    # If something goes very wrong and the stat can't be updated for some reason
    doLog(warn(f"WARNING: failed to update {statistic}, will no longer attempt to update this statistic for this instance.", gvars), gvars)
    gvars.failedStats.append(statistic)
    return False
