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

from os.path import expanduser
from sys import platform
from colored import fg, attr
from typing import NoReturn
from .misc import defineSavePath
global defaultConfig, VERSION

defaultConfig = {
    "blacklist": [
        "claim",
        "claiming",
        "claim -- this was a automated action. please contact me with any questions.",
        "done",
        "done -- this was a automated action. please contact me with any questions.",
        "unclaim",
        "unclaiming",
        "unclaim -- this was a automated action. please contact me with any questions."
    ],
    "caseSensitive": False,
    "cutoff": 1,
    "cutoffUnit": 3600,
    "limit": 100,
    "logUpdates": True,
    "os": platform,
    "printLogs": True,
    "recur": True,
    "regexBlacklist": [
        "^claim(?!(.|\n)*treasure[\s-]*hunt)",
        "^done(?!(.|\n)*treasure[\s-]*hunt)",
        "^unclaim(?!(.|\n)*treasure[\s-]*hunt)"
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
    "useRegex": False,
    "userList": [
        "transcribersofreddit"
    ],
    "wait": 10
}

VERSION = "2.0.0-dev27-20210614"

class Colours():
    def __init__(self: object, warning: int, reset: int) -> NoReturn:
        self.WARNING = fg(warning)
        self.RESET = attr(reset)

class Globals():
    def __init__(self: object, VERSION: int) -> NoReturn:
        self.config = {}
        self.ConsoleColours = Colours(130, 0)
        self.HOME = expanduser("~")
        self.log = []
        self.SAVE_PATH = defineSavePath(self.HOME)
        self.Stats = Statistics()
        self.VERSION = VERSION

class Statistics():
    def __init__(self: object) -> NoReturn:
        self.data = {
            "current": {
                "counted": 0,
                "deleted": 0,
                "waitingFor": 0
            },
            "total": {}
        }
        self.failed = False
    
    def generateNewTotals(self: object) -> NoReturn:
        self.data["total"] = {
                    "counted": 0,
                    "deleted": 0
            }
    
    def resetCurrent(self: object) -> NoReturn:
        self.data["current"] = {
                "counted": 0,
                "deleted": 0,
                "waitingFor": 0
            }
    
    def updateTotals(self: object) -> NoReturn:
        for statistic in ["counted","deleted"]:
            self.data["total"][statistic] += self.data["current"][statistic]

def initialiseGlobals(VERSION: int) -> object:
    return Globals(VERSION)
