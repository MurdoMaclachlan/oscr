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

global version

version = "2.0.0-dev5-20210215"

class Globals():
    def __init__(self, version):
        self.config = {}
        self.failedStats = []
        self.home = expanduser("~")
        self.log = []
        self.version = version

def initialiseGlobals(version):
    
    global gvars
    gvars = Globals(version)
    return gvars
