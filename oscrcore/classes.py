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
    along with this program. If not, see https://www.gnu.org/licenses/.

    Contact me at murdomaclachlan@duck.com

    ----------

    This module contains all classes used by OSCR.
"""

from colored import fg, attr
from datetime import datetime
from os import environ, mkdir
from os.path import expanduser, isdir
from sys import platform
from time import time
from typing import Any, Dict, List, NoReturn, Union
from .globals import DEFAULT_CONFIG, VERSION

global Globals, Log, Stats, System


class GlobalsHandler:
    """The Globals class contains essential miscellaneous global variables that don't
    belong in any of the other three classes. Currently, that means the config settings,
    the version number and the default config.
    """
    def __init__(self: object, default_config: Dict, version: str) -> NoReturn:
        self.__config = {}
        self.DEFAULT_CONFIG = default_config
        self.VERSION = version

    def get(self: object, key: str = None) -> NoReturn:
        """Gets a single config value from a given key.

        Arguments:
        - key (string)

        Returns: the value in the config at the given key
        """
        return self.__config[key] if key else self.__config

    def set(self: object, value: Any, key: str = None) -> NoReturn:
        """Sets a single config key to a single new given value.

        :argument key: (string)
        :argument value: (any type)

        :return: Nothing
        """
        if key:
            self.__config[key] = value
        else:
            self.__config = value

    def snake_case(self: object) -> object:
        """Convert all config keys to snake case.

        Regexes taken from this StackOverflow answer:
        https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case#1176023

        :return: an array containing self and a boolean flag indicating whether or not
            any keys were changed
        """
        import re
        # First run through the keys and add in the underlines
        before = self.__config
        for pattern in [
            re.compile(r'(.)([A-Z][a-z]+)'),
            re.compile(r'([a-z0-9])([A-Z])')
        ]:
            keys = [key for key in self.__config]
            for key in keys:
                self.__config[re.sub(pattern, r'\1_\2', key)] = self.__config.pop(key)
        # Then run through again, converting everything to lowercase
        keys = [key for key in self.__config]
        for key in keys:
            self.__config[key.casefold()] = self.__config.pop(key)
        # Return the entire globals object alongside a flag to determine if any keys
        # were changed by the function
        return [self, True if before != self.__config else False]


class LogHandler:
    """The Log class handles the logging system, surprise surprise. In addition to
    containing the main log array, Log contains data relating to the colouring of log
    output, and also defines a simple API for access and modification to/of the data
    contained therein.
    """
    def __init__(self: object) -> NoReturn:
        self.ConsoleColours = self.Colours(1, 0, 130)
        self.__log = []

    class Colours:
        """The Colours class stores colour attributes which can be applied to strings in
        order to colour the console output of log entries.
        """
        def __init__(self: object, error: int, normal: int, warning: int) -> NoReturn:
            self.ERROR = fg(error)
            self.NORMAL = attr(normal)
            self.WARNING = fg(warning)

    def get_time(self: object, time: int = time()) -> str:
        """Gets the current time and parses it to a human-readable format.

        Arguments:
        - time (int): optional with 'time.time()' as default

        Returns: a single date string in format 'YYYY-MM-DD HH:MM:SS'.
        """
        return datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")

    def new(self: object, messages: Union[List[str], str]) -> bool:
        """Initiates a new log entry and prints it to the console, if printLogs is
        enabled.

        Arguments:
        - messages (string array, or single string)

        Returns: boolean success status.
        """
        if type(messages) == list:
            for message in messages:
                self.process(message)
        else:
            self.process(messages)

        return True

    def process(self: object, message: str) -> bool:
        """Processes a single new log entry. Helper method for Log.new() in case of a
        string array being passed.

        Arguments:
        - messages (single string)

        Returns: boolean success status.
        """
        # Allows for dynamic passing of lists
        if not message:
            return False

        statement = f"{self.get_time()} - {message}"
        self.__log.append(statement)
        print(statement) if Globals.get("print_logs") else None

        return True

    def request(self: object, mode: List) -> Union[List[str], NoReturn, str]:
        """Returns or deletes item(s) in the log, either all items or the most
        recently-added item.

        Arguments:
        - mode (string array of length 2): options;
            - options for the first item are "clear" and "get",
            - options for the second item are "all" and "recent",

        Returns: a single log entry (string), list of log entries (string array), or
                 nothing.
        """
        requests = {
            "all": (self.__log, self.__log[:])[1 if mode[0] == "clear" else 0],
            "recent": self.__log[len(self.__log) - 1],
        }

        try:
            if mode[0] == "clear":
                del requests[mode[1]]
            elif mode[0] == "get":
                return requests[mode[1]]
        except KeyError:
            print(self.warning("WARNING: Log.request() received unknown mode '{i}'."))

    def warning(self: object, message: str) -> str:
        """WARNING: soon-to-be deprecated.

        Creates and returns a string that when printed will be coloured with the warning
        colour.

        Arguments:
        - message (string)

        Returns: a single coloured string.
        """
        return self.ConsoleColours.WARNING + message + self.ConsoleColours.NORMAL


class StatsHandler:
    """The Statistics class stores the current and total statistics and provides a
    simple API for accessing and modifying the data contained therein.
    """
    def __init__(self: object) -> NoReturn:
        self.__data = {
            "current": {"counted": 0, "deleted": 0, "waiting_for": 0},
            "total": {},
        }
        self.enabled = True

    def get(self: object, dataset: str, stat: str = None) -> Union[Dict, int]:
        """Returns either a single statistic or, if no statistic is specified, an entire
        dataset.
        - Dataset options are: "current", "total"
        - Statistic options are: "counted", "deleted", "waitingFor"
          ("waitingFor" is only available for the "current" dataset)

        Arguments:
        - dataset (string)
        - stat (string): optional; default is an empty string

        Returns: a single dictionary or integer.
        """
        return self.__data[dataset][stat] if stat else self.__data[dataset]

    def generate_new(self: object) -> NoReturn:
        """Resets all statistics in the "total" dataset to  0. Should only be used if
        the stats file cannot be found.

        No arguments.

        No return value.
        """
        self.__data["total"] = {"counted": 0, "deleted": 0}

    def increment(self: object, stat: str) -> NoReturn:
        """Increments a single statistic of the "current" dataset.

        Arguments:
        - stat (string)

        No return value.
        """
        self.__data["current"][stat] += 1

    def reset(self: object) -> NoReturn:
        """Resets all entries in the "current" dataset to 0. Should be called every
        program loop.

        No arguments.

        No return value.
        """
        self.__data["current"] = {"counted": 0, "deleted": 0, "waitingFor": 0}

    def set_totals(self: object, totals: Dict) -> NoReturn:
        """Sets the "total" dataset to a new given set of values.

        Arguments:
        - totals (dictionary)

        No return value.
        """
        self.__data["total"] = totals

    def update_totals(self: object) -> NoReturn:
        """Adds the "counted" and "deleted" statistics in the "current" dataset to those
        in the "total" dataset.

        No arguments.

        No return value.
        """
        for statistic in ["counted", "deleted"]:
            self.__data["total"][statistic] += self.__data["current"][statistic]


class SysHandler:
    """The System class handles the most important variables to do with file-handling.
    The paths to the data and config directories are contained here, as well as the
    location of the home directory and the auto-detected OS.
    """
    def __init__(self: object) -> NoReturn:
        self.HOME = expanduser("~")
        self.OS = platform
        self.PATHS = self.define_paths(self.HOME, self.OS)

    def define_paths(self: object, home: str, os: str) -> Dict[str, str]:
        """Detects OS and defines the appropriate save paths for the config and data.
        Exits on detecting an unspported OS. Supported OS's are: Linux, MacOS, Windows.

        Arguments:
        - home (string)
        - os (string)

        Returns: a single string dict containing the newly-defined paths
        """
        os = "".join(list(os)[:3])

        # Route for a supported operating system
        if os in ["dar", "lin", "win"]:

            # Windows is fucking stupid why would you use backslashes what the fuck is
            # AppData why can't you just be normal
            paths = (
                {
                    "config": environ["APPDATA"] + "\\oscr",
                    "data": environ["APPDATA"] + "\\oscr\data",
                }
                if os == "win"
                else {"config": home + "/.config/oscr", "data": home + "/.oscr/data"}
            )

            # Create any missing paths/directories.  This is a horrible bit of code but
            # I'm not sure how to make it any nicer
            for path in paths:
                if not isdir(paths[path]):
                    Log.new(f"Making path: {paths[path]}")
                    for directory in paths[path].split("/")[1:]:
                        current_dir = paths[path].split(directory)[0] + directory
                        if not isdir(current_dir):
                            Log.new(f"Making directory: {current_dir}")
                            mkdir(current_dir)
            return paths

        # Exit if the operating system is unsupported
        else:
            Log.new(Log.warning(f"Unsupported operating system: {os}, exiting."))
            exit()


# Declare global classes
Globals = GlobalsHandler(DEFAULT_CONFIG, VERSION)
Log = LogHandler()
Stats = StatsHandler()
System = SysHandler()
