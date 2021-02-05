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

from .log import doLog

def fetch(statistic, gvars):
    
    result = []

    # If stats.txt doesn't exist, this returns 0. Otherwise it reads the file.
    try:    
        with open(gvars.home+"/.oscr/data/stats.txt", "r") as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        doLog(f"No stats for {statistic} found; returning 0.", gvars)
        return 0

    # If it can't find a value for any statistic, this returns 0.
    if content == []:
        doLog(f"No stats for {statistic} found; returning 0.", gvars)
        return 0
    
    for line in content:
        
        # If it can find the value for the statistic being fetched, this returns it. (I swear this shithole of a for-if-for-if tree must be condensable)
        if list(line)[0] == list(statistic)[0]:
            for i in list(line):
                if i.isnumeric():
                    result.append(str(i))
            break

    # If it can only find one statistic, and it isn't the one being fetched, this returns 0.
    if result == []:          
        doLog(f"No stats for {statistic} found; returning 0.", gvars)
        return 0

    doLog(f"Fetched {statistic} successfully.", gvars)
    return int(''.join(result))

def update(statistic, value, gvars):

    if statistic in gvars.failedStats:
        doLog(f"Skipping update of following statistic: {statistic}", gvars)
        return False
 
    lineToReplace = 0
    newLine = f"{statistic}: {str(value)}"

    # Creates the stats.txt file if it doesn't exist.
    try:
        with open(gvars.home+"/.oscr/data/stats.txt", "r") as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        doLog("No stats.txt found; creating.", gvars)
        content = None

    with open(gvars.home+"/.oscr/data/stats.txt", "w") as file:
        
        # If it can't find any statistics, this adds the statistic to be updated and sets the other to 0.
        if content == None:
            if statistic == "counted":
                file.write(newLine+"\ndeleted: 0")
            else:
                file.write("counted: 0\n"+newLine)
            doLog(f"Updated {statistic} successfully.", gvars)
            return True

        for line in content:
            
            # If it can find both statistics, this updates as normal.
            if list(line)[0] == list(statistic)[0]:
                lineToReplace = content.index(line)
                content[lineToReplace] = newLine
                file.write('\n'.join(content))
                doLog(f"Updated {statistic} successfully.", gvars)
                return True
            
        # If it can only find one statistic, and it isn't the right one, this adds the right one.
        content.append(newLine)
        file.seek(0)
        file.write('\n'.join(content))
        doLog(f"Updated {statistic} successfully.", gvars)
        return True
    
    doLog(f"Statistics error: failed to update {statistic}, will no longer attempt to update this statistic for this instance.")
    gvars.failedStats.append(statistic)
    return False
