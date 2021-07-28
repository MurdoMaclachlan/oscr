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

from os import remove
from os.path import isfile
from configparser import ConfigParser
from typing import Dict, List, Union
from .globals import Globals, Log, System
from .misc import filterArray, writeToFile
global Globals, Log, System

"""
    I'm going to be so happy when I get to
    delete half of this module next version.
"""

# Creates new ini file based on user input
def createIni() -> bool:
    
    Log.new(["praw.ini missing, incomplete or incorrect. It will need to be created."])
    iniVars = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": Globals.config["user"], # Since createIni is never called before the config is initialised, this is safe to draw from
        "password": input("Please input your Reddit password:  ")
    }
    
    # Writes contents to appropriate ini location
    with open(f"{System.PATHS['config']}/praw.ini", "a+") as file:
        file.write("[oscr]\n")
        for i in iniVars: file.write(i+"="+iniVars[i]+"\n")
    
    return True

# Extracts OSCR content from an ini file, returning False if none found
def extractIniDetails() -> Union[bool, List]:
    
    with open(f"{System.PATHS['config']}/../praw.ini", "r+") as file:
        content = file.read().splitlines()
    return False if not content or not oscrOnly(content) else oscrOnly(content) # return None if praw.ini has no OSCR

# Use configparser magic to get the credentials from praw.ini
def getCredentials() -> Dict:
   
    credentials = ConfigParser()
    credentials.read(f"{System.PATHS['config']}/praw.ini")
    return dict(credentials["oscr"])

# Given a list of strings, finds OSCR content as per .ini syntax
# Replaces any CDRemover content with OSCR content
def oscrOnly(content: List) -> List:

    oscrContent = []
    append = False
    for line in content:
        if line.startswith("[") and not line in ["[oscr]", "[oscr]          "]:
            append = False
        elif line in ["[cdrcredentials]", "[oscr]", "[oscr]          "]:
            append = True
        if line == "[cdrcredentials]":
            Log.new([f"Replacing line '{line}' with '[oscr]'."])
            line = "[oscr]"
        if append: oscrContent.append(line)
    return oscrContent

# Reformats the ini file to a new location, changing any CDRemover content to OSCR
# Set to be deprecated in 2.1.0
def reformatIni(Globals: object) -> bool:

    try: getCredentials(Globals)["client_id"]; return True
    except (FileNotFoundError, KeyError): pass
    
    try:
        with open(f"{System.PATHS['config']}/../praw.ini", "r+") as file:
            content = file.read().splitlines()
        oscrContent = oscrOnly(content)
        
        # If no OSCR content was found
        if not oscrContent:
            if isfile(f"{System.PATHS['config']}/praw.ini"):
                Log.new(["praw.ini already formatted."])
                return True
            else: createIni(Globals)
        
        # Else, write all OSCR content to new file
        else:
            with open(f"{System.PATHS['config']}/../praw.ini", "w+") as file:
                success = writeToFile(oscrContent, open(f"{System.PATHS['config']}/praw.ini", "w+"))
                    
        # Remove OSCR section from old praw.ini, and remove file if no other sections are present
        try:
            strippedContent = stripOSCR(content)
            remove(f"{System.PATHS['config']}/../praw.ini")
            writeToFile(strippedContent, open(f"{System.PATHS['config']}/../praw.ini", "w+"))
            with open(f"{System.PATHS['config']}/../praw.ini", "r") as file:
                delete = True if not file.readlines() else False
            if delete: remove(f"{System.PATHS['config']}/../praw.ini")
        except IndexError: pass
        
        return True if success else createIni()

    # Catch missing praw.ini                
    except FileNotFoundError:
        if isfile(f"{System.PATHS['config']}/praw.ini"):
            Log.new(["praw.ini already formatted."])
            return False
        else: return createIni()

# Strips .ini content of any OSCR content
def stripOSCR(content: List) -> List:
    delete = False
    linesToDelete = []
    for line in content:
        if line in ["[oscr]", "[oscr]          "]: delete = True
        elif line.startswith("["): delete = False
        if delete: linesToDelete.append(line)
    return filterArray(content, linesToDelete)
