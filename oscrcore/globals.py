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

    This module contains the basic global variables used by OSCR.
"""

from datetime import datetime
from os import environ, mkdir
from os.path import expanduser, isdir
from sys import platform
from colored import fg, attr
from time import time
from typing import Any, Dict, List, NoReturn, Union
global DEFAULT_CONFIG, Globals, Log, Stats, System, VERSION

DEFAULT_CONFIG = {
    "blacklist": [
        "claim",
        "claiming",
        "claim -- this was a automated action. please contact me with any questions.",
        "dibs",
        "done",
        "done -- this was a automated action. please contact me with any questions.",
        "unclaim",
        "unclaiming",
        "unclaim -- this was a automated action. please contact me with any questions."
    ],
    "caseSensitive": False,
    "cutoff": 1,
    "cutoffUnit": 3600,
    "debug": False,
    "limit": 100,
    "logUpdates": True,
    "os": platform,
    "printLogs": True,
    "recur": True,
    "regexBlacklist": [
        "^(claim|done|dibs|unclaim)(?!(.|\\n)*(treasure[\\s-]*hunt|save))"
    ],
    "reportTotals": True,
    "subredditList": [
        "transcribersofreddit"
    ],
    "unit": [
        "minute",
        "minutes",
        60
    ],
    "useRefreshTokens": False,
    "useRegex": False,
    "userList": [
        "transcribersofreddit"
    ],
    "wait": 10
}

VERSION = "2.2.0-dev2-20211117"


class Globals:
    """The Globals class contains essential miscellaneous global variables that don't
    belong in any of the other three classes. Currently, that means the config settings,
    the version number and the default config.

    WARNING: Globals.config will soon be made private. All write calls should go through
    editConfig(). A getConfig() will soon be implemented for read access.
    """ 
    def __init__(self: object) -> NoReturn:
        self.config = {}
        self.VERSION = VERSION
    

    def editConfig(self: object, key: str, value: Any) -> NoReturn:
        """Sets a single config key to a single new given value. All write commands to
        the config should go through this call.

        Arguments:
        - key (string)
        - value (any type)

        No return value.
        """
        self.config[key] = value


class Log:
    """The Log class handles the logging system, surprise surprise. In addition to
    containing the main log array, Log contains data relating to the colouring of log
    output, and also defines a simple API for access and modification to/of the data
    contained therein.
    """  
    def __init__(self: object) -> NoReturn:
        self.ConsoleColours = self.Colours(130, 0)
        self.__log = []
    
    class Colours:
        """The Colours class stores colour attributes which can be applied to strings in
        order to colour the console output of log entries.
        """
        def __init__(self: object, warning: int, reset: int) -> NoReturn:
            self.RESET = attr(reset)
            self.WARNING = fg(warning)
    
    def getTime(self: object, timeToFind: int) -> str:
        """Gets the current time and parses it to a human-readable format.

        Arguments:
        - time (int): optional with 'time.time()' as default

        Returns: a single date string in format 'YYYY-MM-DD HH:MM:SS'.
        """
        return datetime.fromtimestamp(timeToFind).strftime("%Y-%m-%d %H:%M:%S")
    
    def new(self: object, messages: Union[List[str], str]) -> bool:
        """Initiates a new log entry and prints it to the console, if printLogs is
        enabled.

        Arguments:
        - messages (string array)

        Returns: boolean success status.
        """
        for message in messages:
            
            # Allows for dynamic passing of lists
            if not message: continue
            
            currentTime = self.getTime(time())
            
            self.__log.append(f"{currentTime} - {message}\n")
            print(f"{currentTime} - {message}") if Globals.config["printLogs"] else None
        
        return True

    def request(self: object, mode: List) -> NoReturn:
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
            "recent": self.__log[len(self.__log)-1]
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
        return self.ConsoleColours.WARNING + message + self.ConsoleColours.RESET


class Statistics:
    """The Statistics class stores the current and total statistics and provides a
    simple API for accessing and modifying the data contained therein.
    """
    def __init__(self: object) -> NoReturn:
        self.__data = {
            "current": {
                "counted": 0,
                "deleted": 0,
                "waitingFor": 0
            },
            "total": {}
        }
        self.enabled = True
    
    def get(self: object, dataset: str, stat="") -> int:
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
        if not stat:
            return self.__data[dataset]
        else:
            return self.__data[dataset][stat]
    
    def generateNew(self) -> NoReturn:
        """Resets all statistics in the "total" dataset to  0. Should only be used if
        the stats file cannot be found.

        No arguments.

        No return value.
        """
        self.__data["total"] = {
                "counted": 0,
                "deleted": 0
        }
    
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
        self.__data["current"] = {
                "counted": 0,
                "deleted": 0,
                "waitingFor": 0
        }
    
    def setTotals(self: object, totals: Dict) -> NoReturn:
        """Sets the "total" dataset to a new given set of values.

        Arguments:
        - totals (dictionary)

        No return value.
        """
        self.__data["total"] = totals
    
    def updateTotals(self: object) -> NoReturn:
        """Adds the "counted" and "deleted" statistics in the "current" dataset to those
        in the "total" dataset.

        No arguments.

        No return value.
        """
        for statistic in ["counted", "deleted"]:
            self.__data["total"][statistic] += self.__data["current"][statistic]


class System:
    """The System class handles the most important variables to do with file-handling.
    The paths to the data and config directories are contained here, as well as the
    location of the home directory and the auto-detected OS.
    """
    def __init__(self: object) -> NoReturn:
        self.HOME = expanduser("~")
        self.OS = platform
        self.PATHS = self.definePaths(self.HOME, self.OS)
    
    def definePaths(self: object, home: str, os: str) -> List:
        """Detects OS and defines the appropriate save paths for the config and data.
        Exits on detecting an unspported OS. Supported OS's are: Linux, MacOS, Windows.

        Arguments:
        - home (string)
        - os (string)

        Returns: a single string array containing the newly-
                 defined paths
        """
        os = ''.join(list(os)[:3])
        
        if os in ["dar", "lin", "win"]:
            
            # Windows is fucking stupid why would you use backslashes
            # what the fuck is AppData why can't you just be normal
            paths = {
                "config": environ["APPDATA"] + "\\oscr",
                "data": environ["APPDATA"] + "\\oscr\data"
            } if os == "win" else {
                "config": home + "/.config/oscr",
                "data": home + "/.oscr/data"
            }
                
            # Create any missing paths/directories
            for path in paths:
                if not isdir(paths[path]):
                    Log.new(f"Making path: {paths[path]}")
                    for directory in paths[path].split("/")[1:]:
                        if not isdir(paths[path].split(directory)[0] + directory):
                            Log.new(f"Making directory: {paths[path].split(directory)[0]}{directory}")
                            mkdir(paths[path].split(directory)[0] + directory)
            return paths
        
        # Exit is OS is unsupported
        else:
            Log.new(Log.warning(f"Unsupported operating system: {os}, exiting."))
            exit()
      

# Declare global classes
Globals = Globals()
Log = Log()
Stats = Statistics()
System = System()
