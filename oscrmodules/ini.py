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
from .log import doLog
from .misc import filterArray, writeToFile

def createIni(Globals):
    
    doLog(["praw.ini missing, incomplete or incorrect. It will need to be created."], Globals)
    iniVars = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": Globals.config["user"], # Since createIni is never called before the config is initialised, this is safe to draw from
        "password": input("Please input your Reddit password:  ")
    }
    with open(Globals.SAVE_PATH+"/oscr/praw.ini", "a+") as file:
        file.write("[oscr]\n")
        for i in iniVars: file.write(i+"="+iniVars[i]+"\n")
    return True

def extractIniDetails(Globals):
    with open(Globals.SAVE_PATH+"/praw.ini", "r+") as file:
        content = file.read().splitlines()
        return None if content == [] or oscrOnly(content, Globals) == [] else oscrOnly(content, Globals) # return None if praw.ini has no OSCR

def getCredentials(Globals):
    
    # Use configparser magic to get the credentials from praw.ini
    credentials = ConfigParser()
    credentials.read(Globals.SAVE_PATH + "/oscr/praw.ini")
    return dict(credentials["oscr"])
   
def oscrOnly(content, Globals):
    oscrContent = []
    append = False
    for line in content:
        if line.startswith("[") and not line in ["[oscr]", "[oscr]          "]:
            append = False
        elif line in ["[cdrcredentials]", "[oscr]", "[oscr]          "]:
            append = True
        if line == "[cdrcredentials]":
            doLog([f"Replacing line '{line}' with '[oscr]'."], Globals)
            line = "[oscr]"
        if append: oscrContent.append(line)
    return oscrContent

def reformatIni(Globals):

    try: getCredentials(Globals)["client_id"]; return True
    except (FileNotFoundError, KeyError): pass
    
    try:
        with open(Globals.SAVE_PATH+"/praw.ini", "r+") as file:
            content = file.read().splitlines()
        oscrContent = oscrOnly(content, Globals)
        
        # If no OSCR content was found
        if oscrContent is None:
            if isfile(Globals.SAVE_PATH+"/oscr/praw.ini"):
                doLog(["praw.ini already formatted."], Globals)
                return True
            else: createIni(Globals)
        
        # Else, write all OSCR content to new file
        else:
            with open(Globals.SAVE_PATH+"/praw.ini", "w+") as file:
                success = writeToFile(Globals, oscrContent, open(Globals.SAVE_PATH+"/oscr/praw.ini", "w+"))
                    
        # Remove OSCR section from old praw.ini, and remove file if no other sections are present
        try:
            strippedContent = stripOSCR(content)
            remove(Globals.SAVE_PATH+"/praw.ini")
            writeToFile(Globals, strippedContent, open(Globals.SAVE_PATH+"/praw.ini", "w+"))
            with open(Globals.SAVE_PATH+"/praw.ini", "r") as file:
                delete = True if file.readlines() == [] else False
            if delete: remove(Globals.SAVE_PATH+"/praw.ini")
        except IndexError: pass
        
        return True if success else createIni(Globals)

    # Catch missing praw.ini                
    except FileNotFoundError:
        if isfile(Globals.SAVE_PATH + "/praw.ini"):
            doLog(["praw.ini already formatted."], Globals)
        else: createIni(Globals)

def stripOSCR(content):
    delete = False
    linesToDelete = []
    for line in content:
        if line in ["[oscr]", "[oscr]          "]: delete = True
        elif line.startswith("["): delete = False
        if delete: linesToDelete.append(line)
    return filterArray(content, linesToDelete)
    
