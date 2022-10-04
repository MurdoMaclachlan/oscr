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

from os import environ, makedirs
from os.path import expanduser, isdir
from sys import platform
from typing import Any, Dict, Union
from .globals import DEFAULT_CONFIG, VERSION

global Globals, Stats, System


class GlobalsHandler:
    """The Globals class contains essential miscellaneous global variables that don't
    belong in any of the other three classes. Currently, that means the config settings,
    the version number and the default config.
    """
    def __init__(self: object, default_config: Dict, version: str) -> None:
        self.__config = {}
        self.DEFAULT_CONFIG = default_config
        self.VERSION = version

    def get(self, key: str = None) -> None:
        """Gets a single config value from a given key.

        Arguments:
        - key (string)

        Returns: the value in the config at the given key
        """
        return self.__config[key] if key else self.__config

    def set(self, value: Any, key: str = None) -> None:
        """Sets a single config key to a single new given value.

        :argument key: (string)
        :argument value: (any type)

        :return: Nothing
        """
        if key:
            self.__config[key] = value
        else:
            self.__config = value

    def snake_case(self) -> object:
        """Convert all config keys to snake case.

        Regexes taken from this StackOverflow answer:
        https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case#1176023

        :return: an array containing self and a boolean flag indicating whether any keys
                 were changed
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


class StatsHandler:
    """The Statistics class stores the current and total statistics and provides a
    simple API for accessing and modifying the data contained therein.
    """
    def __init__(self) -> None:
        self.__data: dict[str, dict] = {
            "current": {"counted": 0, "deleted": 0, "waiting_for": 0},
            "total": {},
        }
        self.enabled = True

    def get(self, dataset: str, stat: str = None) -> Union[Dict, int]:
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

    def generate_new(self) -> None:
        """Resets all statistics in the "total" dataset to  0. Should only be used if
        the stats file cannot be found.

        No arguments.

        No return value.
        """
        self.__data["total"] = {"counted": 0, "deleted": 0}

    def increment(self, stat: str) -> None:
        """Increments a single statistic of the "current" dataset.

        Arguments:
        - stat (string)

        No return value.
        """
        self.__data["current"][stat] += 1

    def reset(self) -> None:
        """Resets all entries in the "current" dataset to 0. Should be called every
        program loop.

        No arguments.

        No return value.
        """
        self.__data["current"] = {"counted": 0, "deleted": 0, "waiting_for": 0}

    def set_totals(self, totals: Dict) -> None:
        """Sets the "total" dataset to a new given set of values.

        Arguments:
        - totals (dictionary)

        No return value.
        """
        self.__data["total"] = totals

    def update_totals(self) -> None:
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
    def __init__(self) -> None:
        self.HOME = expanduser("~")
        self.OS = platform
        self.PATHS = self.__define_paths(self.HOME, self.OS)

    def __define_paths(self, home: str, os: str) -> Dict[str, str]:
        """Detects OS and defines the appropriate save paths for the config and data.
        Exits on detecting an unsupported OS. Supported OSes are: Linux, MacOS, Windows.

        Arguments:
        - home (string)
        - os (string)

        Returns: a single string dict containing the newly-defined paths
        """
        os = "".join(list(os)[:3])

        # Route for a supported operating system
        if os in ["dar", "lin", "win"]:

            paths = (
                {
                    "config": environ["APPDATA"] + "\\oscr",
                    "data": environ["APPDATA"] + "\\oscr\data"
                } if os == "win" else {
                    "config": f"{home}/.config/oscr",
                    "data": f"{home}/.config/oscr/data"
                }
            )

            # Create any missing paths/directories
            for path in paths:
                if not isdir(paths[path]):
                    print(f"Making path: {paths[path]}")
                    makedirs(paths[path], exist_ok=True)
            return paths

        # Exit if the operating system is unsupported
        else:
            print(f"FATAL: Unsupported operating system: {os}, exiting.")
            exit()


# Declare global classes
Globals = GlobalsHandler(DEFAULT_CONFIG, VERSION)
Stats = StatsHandler()
System = SysHandler()
