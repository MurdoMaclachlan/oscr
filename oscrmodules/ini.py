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

def createIni(gvars):
    
    doLog(["praw.ini missing, incomplete or incorrect. It will need to be created."], gvars)
    iniVars = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": gvars.config["user"], # Since createIni is never called before the config is initialised, this is safe to draw from
        "password": input("Please input your Reddit password:  ")
    }
    with open(gvars.SAVE_PATH+"/oscr/praw.ini", "a+") as file:
        file.write("[oscr]\n")
        for i in iniVars: file.write(i+"="+iniVars[i]+"\n")
    return True

def extractIniDetails(gvars):
    with open(gvars.SAVE_PATH+"/praw.ini", "r+") as file:
        content = file.read().splitlines()
        return None if content == [] or oscrOnly(content, gvars) == [] else oscrOnly(content, gvars) # return None if praw.ini has no OSCR

def getCredentials(gvars):
    
    # Use configparser magic to get the credentials from praw.ini
    credentials = ConfigParser()
    credentials.read(gvars.SAVE_PATH + "/oscr/praw.ini")
    return dict(credentials["oscr"])
   
def oscrOnly(content, gvars):
    oscrContent = []
    append = False
    for line in content:
        if line.startswith("[") and not line in ["[oscr]", "[oscr]          "]:
            append = False
        elif line in ["[cdrcredentials]", "[oscr]", "[oscr]          "]:
            append = True
        if line == "[cdrcredentials]":
            doLog([f"Replacing line '{line}' with '[oscr]'."], gvars)
            line = "[oscr]"
        if append: oscrContent.append(line)
    return oscrContent

def reformatIni(gvars):

    try: getCredentials(gvars)["client_id"]; return True
    except (FileNotFoundError, KeyError): pass
    
    try:
        with open(gvars.SAVE_PATH+"/praw.ini", "r+") as file:
            content = file.read().splitlines()
        oscrContent = oscrOnly(content, gvars)
        
        # If no OSCR content was found
        if oscrContent is None:
            if isfile(gvars.SAVE_PATH+"/oscr/praw.ini"):
                doLog(["praw.ini already formatted."], gvars)
                return True
            else: createIni(gvars)
        
        # Else, write all OSCR content to new file
        else:
            with open(gvars.SAVE_PATH+"/praw.ini", "w+") as file:
                success = writeToFile(gvars, oscrContent, open(gvars.SAVE_PATH+"/oscr/praw.ini", "w+"))
                    
        # Remove OSCR section from old praw.ini, and remove file if no other sections are present
        try:
            strippedContent = stripOSCR(content)
            remove(gvars.SAVE_PATH+"/praw.ini")
            writeToFile(gvars, strippedContent, open(gvars.SAVE_PATH+"/praw.ini", "w+"))
            with open(gvars.SAVE_PATH+"/praw.ini", "r") as file:
                delete = True if file.readlines() == [] else False
            if delete: remove(gvars.SAVE_PATH+"/praw.ini")
        except IndexError: pass
        
        return True if success else createIni(gvars)

    # Catch missing praw.ini                
    except FileNotFoundError:
        if isfile(gvars.SAVE_PATH + "/praw.ini"):
            doLog(["praw.ini already formatted."], gvars)
        else: createIni(gvars)

def stripOSCR(content):
    delete = False
    linesToDelete = []
    for line in content:
        if line in ["[oscr]", "[oscr]          "]: delete = True
        elif line.startswith("["): delete = False
        if delete: linesToDelete.append(line)
    return filterArray(content, linesToDelete)
    
