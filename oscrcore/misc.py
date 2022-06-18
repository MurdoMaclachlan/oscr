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

    This module is divided into several categories, which is probably
    contradictory to its classification as "misc", but it's my module
    and I'll modulate it however I please.
"""

import json
import sys
from typing import Dict, List, TextIO
from .classes import Globals, System
from .logger import Log

global Globals, Log, System


"""
    CONFIGURATION FUNCTIONS

    These functions are related to the config, including the creation, retrieval and
    management of its values.
"""


def check_config() -> None:
    """Checks if all necessary config options are present and conform the correct format

    No arguments.

    No return value.
    """
    # Check to see if each key in the default config is also in the config file
    # Also call .snake_case() to ensure there are no camel case remnants from earlier
    # versions of OSCR
    current_config = Globals.snake_case()[0].get()
    for key in Globals.DEFAULT_CONFIG:
        if key not in current_config:
            Log.new(
                f"Detected missing config key: {key}. Adding with default value.",
                "WARNING"
            )
            Globals.set(Globals.DEFAULT_CONFIG[key], key=key)
    dump_config()


def dump_config() -> bool:
    """Attempts to dump the config to the config file

    No arguments.

    Returns: boolean success status.
    """
    return dump_json(
        f"{System.PATHS['config']}/config.json", {"config": [Globals.get()]}
    )


def get_config() -> None:
    """Retrieves the config from the config.json file; if no config is found, creates
    one from the default values.

    No arguments.

    No return value.
    """
    try:
        with open(f"{System.PATHS['config']}/config.json") as config_file:
            try:
                data = json.load(config_file)

            # Catch invalid JSON in the config file (usually a result of manual editing)
            except json.decoder.JSONDecodeError as e:
                print(
                    "FATAL: Failed to get config; could not decode JSON file. Exiting.",
                    f"Error was: {e}"
                )
                sys.exit(0)

            Globals.set(data["config"][0])
            check_config()

    # Catch missing config file
    except FileNotFoundError:
        from .globals import DEFAULT_CONFIG

        Globals.set(DEFAULT_CONFIG)
        Globals.set(
            input(
            "No config file found. Please enter your Reddit username:  /u/"
            ),
            key="user"
        )
        dump_config()


"""
    TRUE MISCELLANEOUS

    The following functions don't fit into any real category at all.
"""


def calculate_essentials() -> None:
    """Performs any necessary one-time calculations or changes relating to the config.

    No arguments.

    No return value.
    """
    # Will default any non-numeric limits to 1000.
    if not str(Globals.get("limit")).isnumeric():
        Globals.set(1000, key="limit")

    # Attempts to calculate the cutoff time and wait time in seconds
    for keyList in [
        ["cutoff_sec", "cutoff", "cutoff_unit", 3600],
        ["wait_time", "wait", "unit", 1800],
    ]:
        try:
            Globals.set(
                Globals.get(key=keyList[1]) *
                (
                    Globals.get(key=keyList[2])[2]
                    if type(Globals.get(key=keyList[2])) == list else
                    Globals.get(key=keyList[2])
                ),
                key=keyList[0]
            )

        # Defaults to one hour / half an hour if any of the related variables is missing
        # or corrupted
        except (KeyError, TypeError):
            Globals.get(keyList[3], key=keyList[0])


def check_regex(re, comment: str) -> bool:
    """Checks a given string against all members of the regex blacklist.

    Arguments:
    - re (module)
    - comment (string)

    Returns: boolean.
    """
    for pattern in Globals.get(key="regex_blacklist"):
        if re.match(
            pattern, (comment.casefold(), comment)[Globals.get(key="case_sensitive")]
        ):
            return True
    return False


def dump_json(path: str, data: Dict) -> bool:
    """Dumps dictionary as JSON content to a given path.

    Arguments:
    - path (string)
    - data (dictionary)

    Returns: boolean success status.
    """
    try:
        with open(path, "w") as outFile:
            outFile.write(json.dumps(data, indent=4, sort_keys=True))
        return True
    except FileNotFoundError:
        return False


def filter_array(array: List, elements: List) -> List:
    """Deletes a portion of a given array based on given starting and ending elements.

    Arguments:
    - array (array)
    - elements (array)

    Returns: a single array.
    """
    del array[array.index(elements[0]) : array.index(elements[len(elements) - 1])]
    return array


def write_to_file(content: List, file: TextIO) -> bool:
    """Writes each element of a list as a new line to a given file.

    Arguments:
    - content (list)
    - file (TextIO instance)

    Returns: boolean success status.
    """
    for line in content:
        file.write(line + "\n")
    return True
