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
        "^(claim|done|dibs|unclaim)(?!(.|\n)*treasure[\s-]*hunt)"
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

VERSION = "2.1.0"

"""
    Globals is the miscellaneous global class, containing
    essential variables that don't belong in any of the
    other 3. Currently, that means the config settings and
    the version number.
"""


class Globals:
    
    def __init__(self: object) -> NoReturn:
        self.config = {}
        self.VERSION = VERSION
    
    # Read/write access to the base config may be replaced with a function call soon
    # All edits should go through this function to prevent a breaking change
    def editConfig(self: object, key: str, value: Any) -> NoReturn:
        self.config[key] = value


"""
    Log handles the logging system, surprise surprise. In
    addition to containing the main log array, Log contains
    data relating to the colouring of log output, and also
    defines a simple API for access and modification to/of
    the data contained therein.
"""


class Log:
    
    def __init__(self: object) -> NoReturn:
        self.ConsoleColours = self.Colours(130, 0)
        self.__log = []
    
    # Colour attributes for log highlighting
    class Colours:
        
        def __init__(self: object, warning: int, reset: int) -> NoReturn:
            self.RESET = attr(reset)
            self.WARNING = fg(warning)
    
    # Finds the current time and returns it in a human readable format.
    def getTime(self: object, timeToFind: int) -> str:
        return datetime.fromtimestamp(timeToFind).strftime("%Y-%m-%d %H:%M:%S")
    
    # Updates the log array and prints to console
    def new(self: object, messages: Union[List[str], str]) -> bool:
        
        for message in messages:
            
            # Allows for dynamic passing of lists
            if not message: continue
            
            currentTime = self.getTime(time())
            
            self.__log.append(f"{currentTime} - {message}\n")
            print(f"{currentTime} - {message}") if Globals.config["printLogs"] else None
        
        return True
    
    # Returns or deletes item(s) in the log; either all or the most recent.
    def request(self: object, mode: List) -> NoReturn:
        
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
    
    # Colours a single string orange
    def warning(self: object, message: str) -> str:
        return self.ConsoleColours.WARNING + message + self.ConsoleColours.RESET


"""
    Statistics stores the current and total statistics
    and provides a simple API for accessing and modifying
    the data contained therein.
"""


class Statistics:
    
    def __init__(self: object) -> NoReturn:
        self.__data = {
            "current": {
                "counted": 0,
                "deleted": 0,
                "waitingFor": 0
            },
            "total": {}
        }
        self.failed = False
    
    # Returns either a single statistic or an entire dataset (current/total)
    def get(self: object, dataset: str, stat="") -> int:
        if not stat:
            return self.__data[dataset]
        else:
            return self.__data[dataset][stat]
    
    # Resets total dataset to 0; only use if stats file can't be found
    def generateNew(self) -> NoReturn:
        self.__data["total"] = {
                "counted": 0,
                "deleted": 0
        }
    
    # Increments a single current statistic
    def increment(self: object, stat: str) -> NoReturn:
        self.__data["current"][stat] += 1
    
    # Resets current dataset
    def reset(self: object) -> NoReturn:
        self.__data["current"] = {
                "counted": 0,
                "deleted": 0,
                "waitingFor": 0
        }
    
    # Sets dataset to passed value
    def setTotals(self: object, totals: Dict) -> NoReturn:
        self.__data["total"] = totals
    
    # Updates total dataset using current dataset
    def updateTotals(self: object) -> NoReturn:
        for statistic in ["counted", "deleted"]:
            self.__data["total"][statistic] += self.__data["current"][statistic]


"""
    System class handles the most important variables to
    do with file-handling. The paths to the data and config
    directories are contained here, as well as the location
    of the home directory and the auto-detected OS.
"""


class System:
    
    def __init__(self: object) -> NoReturn:
        self.HOME = expanduser("~")
        self.OS = platform
        self.PATHS = self.definePaths(self.HOME, self.OS)
    
    # Defines save paths for config and data based on the user's OS
    def definePaths(self: object, home: str, os: str) -> List:
        
        # Gets first 3 characters of OS
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
