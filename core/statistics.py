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
from typing import List, NoReturn, TextIO
from .log import doLog, warn
from .misc import dumpJSON

"""
    This module contains file handling for the statistics,
    deleted and counted, including a function to fetch
    the stats at the beginning of run-time, and another
    to update them after each iteration.
"""

# Updates statistics in stats.json
def dumpStats(Globals: object) -> bool:
    
    if dumpJSON(
            Globals.HOME+"/.oscr/data/stats.json",
            {"statistics": [Globals.Stats.data["total"]]}
        ):
        doLog([f"Updated statistics successfully."], Globals)
        return False
    else:
        doLog([warn(f"WARNING: Failed to update statistics, will no longer attempt to update for this instance.", Globals)], Globals)
        return True

# Retrieve statistics from stats.json
def fetchStats(Globals: object) -> object:
    
    try:
        with open(Globals.HOME+"/.oscr/data/stats.json", "r") as file:
            try: data = json.load(file)
            
            # Catch invalid JSON in the config file (usually a result of manual editing)
            except json.decoder.JSONDecodeError as e:
                doLog([warn(f"WARNING: Failed to fetch statistics; could not decode JSON file. Returning 0.", Globals), warn(f"Error was: {e}", Globals)], Globals)
                Globals.Stats.generateNewTotals()
                return Globals
            
            Globals.Stats.data["total"] = data["statistics"][0]
            doLog([f"Fetched statistics successfully."], Globals)
        
    # Catch missing stats file
    except FileNotFoundError:
        doLog([warn(f"WARNING: Could not find stats file. It will be created.", Globals)], Globals)
        Globals.Stats.generateNewTotals()
        Globals.Stats.failed = dumpStats(Globals)
    
    return Globals
