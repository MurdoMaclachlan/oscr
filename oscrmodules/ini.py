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
from .log import doLog

"""
    This module contains handling for the praw.ini file.
"""

def createIni(gvars):
    
    doLog("praw.ini missing, incomplete or incorrect. It will need to be created.", gvars)
    iniVars = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": gvars.config["user"], # Since createIni is never called before the config is initialised, this is safe to draw from
        "password": input("Please input your Reddit password:  ")
    }
    with open(gvars.savePath+"/praw.ini", "a+") as file:
        file.write("[oscr]\n")
        for i in iniVars:
            file.write(i+"="+iniVars[i]+"\n")
    return True

def getCredentials(gvars):
    credentials = ConfigParser()
    credentials.read(gvars.savePath + "/praw.ini")
    return dict(credentials["oscr"])
   
def reformatIni(gvars):
    
    try:
        with open(gvars.home+"/.config/praw.ini", "r+") as file:
            content = file.read().splitlines()
            
            # If praw.ini is empty
            if content == []:
                doLog("praw.ini file is empty. Proceeding to create.", gvars)
                return createIni(gvars)
            
            else:
                success = False
                file.seek(0)
                
                # Replace necessary line and write all lines to file
                for line in content:
                    if line == "[cdrcredentials]":
                        doLog(f"Replacing line '{line}' with '[oscr]'.", gvars)
                        line = "[oscr]          "
                        success = True
                    elif line in ["[oscr]", "[oscr]          "]:
                        success = True
                        doLog("praw.ini file already formatted to OSCR.", gvars)
                    file.write(line+"\n")
                
                # If successfully formatted to OSCR
                if success:
                    return True
                
                # If no cdrcredentials or oscr section was found
                else:
                    doLog("praw.ini file is missing a section for OSCR. Proceeding to create.", gvars)
                    return createIni(gvars)
    
    # Catch missing praw.ini                
    except FileNotFoundError:
        return createIni(gvars)
