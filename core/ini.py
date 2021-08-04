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

from configparser import ConfigParser
from typing import Dict
from .globals import Globals, Log, System
global Globals, Log, System

"""
    This module contains functions relating to the handling
    the praw.ini file.
"""


# Creates new ini file based on user input
def createIni() -> bool:
    
    Log.new(["praw.ini missing, incomplete or incorrect. It will need to be created."])
    iniVars = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": Globals.config["user"],  # Since createIni is never called before the config is initialised, this is safe to draw from
        "password": input("Please input your Reddit password:  ")
    }
    
    # Writes contents to appropriate ini location
    with open(f"{System.PATHS['config']}/praw.ini", "a+") as file:
        file.write("[oscr]\n")
        for i in iniVars: file.write(i+"="+iniVars[i]+"\n")
    
    return True


# Use configparser magic to get the credentials from praw.ini
def getCredentials() -> Dict:
   
    credentials = ConfigParser()
    credentials.read(f"{System.PATHS['config']}/praw.ini")
    return dict(credentials["oscr"])
