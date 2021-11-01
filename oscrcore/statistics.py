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
from typing import NoReturn
from .globals import Globals, Log, Stats, System
from .misc import dumpJSON
global Globals, Log, Stats, System

"""
    This module contains file handling for the statistics,
    deleted and counted, including a function to fetch
    the stats at the beginning of run-time, and another
    to update them after each iteration.
"""


# Updates statistics in stats.json
def dumpStats() -> bool:
    
    if dumpJSON(
            f"{System.PATHS['data']}/stats.json",
            {"statistics": [Stats.get("total")]}
    ):
        Log.new(["Updated statistics successfully."])
        return False
    else:
        Log.new([Log.warning("WARNING: Failed to update statistics, will no longer attempt to update for this instance.")])
        return True


# Retrieve statistics from stats.json
def fetchStats() -> NoReturn:
    
    try:
        with open(f"{System.PATHS['data']}/stats.json", "r") as file:
            try: data = json.load(file)
            
            # Catch invalid JSON in the config file (usually a result of manual editing)
            except json.decoder.JSONDecodeError as e:
                Log.new([Log.warning("WARNING: Failed to fetch statistics; could not decode JSON file. Returning 0."), Log.warning(f"Error was: {e}")])
                Stats.generateNew()
            
            Stats.setTotals(data["statistics"][0])
            Log.new(["Fetched statistics successfully."])
        
    # Catch missing stats file
    except FileNotFoundError:
        Log.new([Log.warning("WARNING: Could not find stats file. It will be created.")])
        Stats.generateNew()
        Stats.failed = dumpStats()


def updateAndLogStats() -> NoReturn:

    # Gives info about most recent iteration; how many comments were counted,
    # deleted, still waiting for.
    Log.new([
        f"Counted this cycle: {Stats.get('current', stat='counted')}",
        f"Deleted this cycle: {Stats.get('current', stat='deleted')}",
        f"Waiting for: {Stats.get('current', stat='waitingFor')}"
    ])

    # Updates total statistics
    Stats.updateTotals()
    Stats.enabled = dumpStats() if Stats.enabled else False
    Log.new([
        f"Total Counted: {str(Stats.get('total', stat='counted'))}",
        f"Total Deleted: {str(Stats.get('total', stat='deleted'))}"
    ]) if Globals.config["reportTotals"] else None
