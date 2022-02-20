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

    This module contains file handling for the statistics "deleted" and
    "counted", including a function to fetch these statistics at the
    beginning of run-time and another to update them after each iteration.
"""

import json
from typing import NoReturn
from .classes import Globals, Log, Stats, System
from .misc import dump_json
global Globals, Log, Stats, System


def dump_stats() -> bool:
    """Writes the total statistics to stats.json.

    No arguments.

    Returns: boolean success status.
    """
    if dump_json(
        f"{System.PATHS['data']}/stats.json", {"statistics": [Stats.get("total")]}
    ):
        Log.new("Updated statistics successfully.")
        return True
    else:
        Log.new(
            Log.warning(
                "WARNING: Failed to update statistics, will no longer attempt to"
                + " update for this instance."
            )
        )
        return False


def fetch_stats() -> NoReturn:
    """Fetches statistics from the stats.json file in the data path.

    No arguments.

    No return value.
    """
    try:
        with open(f"{System.PATHS['data']}/stats.json", "r") as file:
            try:
                data = json.load(file)

            # Catch invalid JSON in the config file (usually a result of manual editing)
            except json.decoder.JSONDecodeError as e:
                Log.new(
                    [
                        Log.warning(
                            "WARNING: Failed to fetch statistics; could not decode"
                            + " JSON file. Returning 0."
                        ),
                        Log.warning(f"Error was: {e}"),
                    ]
                )
                Stats.generate_new()

            Stats.set_totals(data["statistics"][0])
            Log.new("Fetched statistics successfully.")

    # Catch missing stats file
    except FileNotFoundError:
        Log.new(
            Log.warning("WARNING: Could not find stats file. It will be created.")
        )
        Stats.generate_new()
        Stats.enabled = dump_stats()


def update_and_log_stats() -> NoReturn:
    """Logs current statistics and updates and logs totals following an iteration of
    OSCR.

    No arguments.

    No return value.
    """
    # Gives info about most recent iteration; how many comments were counted, deleted,
    # still waiting for.
    Log.new(
        [
            f"Counted this cycle: {Stats.get('current', stat='counted')}",
            f"Deleted this cycle: {Stats.get('current', stat='deleted')}",
            f"Waiting for: {Stats.get('current', stat='waitingFor')}",
        ]
    )

    # Updates total statistics
    Stats.update_totals()
    Stats.enabled = dump_stats() if Stats.enabled else False
    Log.new(
        [
            f"Total Counted: {Stats.get('total', stat='counted')}",
            f"Total Deleted: {Stats.get('total', stat='deleted')}",
        ]
    ) if Globals.get(key="report_totals") else None
