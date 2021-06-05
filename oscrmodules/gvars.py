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
from .misc import defineSavePath
global defaultConfig, version

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
VERSION = "2.0.0-dev21-20210604"

class Globals():
    def __init__(self, VERSION):
        self.config = {}
        self.failedStats = []
        self.home = expanduser("~")
        self.log = []
        self.savePath = defineSavePath(self.home)
        self.version = VERSION
        self.ConsoleColours = Colours(130, 0)

class Colours():
    def __init__(self, warning, reset):
        self.warning = fg(warning)
        self.reset = attr(reset)

def initialiseGlobals(VERSION):
    gvars = Globals(VERSION)
    return gvars
