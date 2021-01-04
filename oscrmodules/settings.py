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

# This whole module is an ugly bastard, but it works
# I'll deal with it eventually probably maybe

import sys
import json
from .log import doLog, updateLog
from .misc import calculateEssentials, createIni

# Main settings menu
# If-tree the first, but not the last
def settingsMain(gvars):

    doLog("Success: reached settings menu.", gvars)

    while True:
        # Gets user choice
        print("\nOPTIONS MENU\n1. Edit config\n2. Edit praw.ini\n3. Continue to program\n4. Exit")
        results = ["1", "2", "3", "4"]
        choice = validateChoice(results)

        # Determines which result happens
        if choice == "1":
            doLog("Opening config edit menu.", gvars)
            editConfig(gvars)
        elif choice == "2":
            doLog("Opening praw.ini edit menu.", gvars)
            doLog("WARNING: edits to praw.ini will require a restart to take effect.", gvars)
            editPraw(gvars)
        elif choice == "3":
            return doLog("Exiting settings menu, continuing to main program.", gvars)
        else:
            updateLog("Updating log...", gvars)
            doLog("Log updated successfully.", gvars)
            updateLog("Exiting OSCR...", gvars)
            sys.exit(0)

# This fucking shite is the bane of my existence
# You'd think I wouldn't need to turn my r/badcode flair into actual fucking code
# But apparently I do
# Does what it says on the fucking tin
def editConfig(gvars):

    # Gets user choice
    print("\nWhich option would you like?\n1. Add to blacklist\n2. Remove from blacklist\n3. Cutoff\n4. Cutoff unit\n5. Limit\n6. Log updates\n7. Operating system\n8. Recur\n9. Add to subredditList\n10. Remove from subredditList\n11. Wait unit\n12. Username\n13. Wait amount\n14. Return to main settings menu")
    results = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
    resultNames = list(gvars.config.keys())
    choice = validateChoice(results)

    # Returns to main settings menu
    if choice == "14":
        return True
    
    # All possible results 
    if choice == "1":
        key = resultNames[int(choice)-1]
    elif int(choice) > 1 and int(choice) < 10:
        key = resultNames[int(choice)-2]
    else:
        key = resultNames[int(choice)-3]
    
    # Adds/removes from blacklist
    if choice in ["1", "2", "9", "10"]:
  
        if choice in ["1", "9"]:
            gvars.config[key].append(input(f"\nPlease enter the phrase to add to the {key}\n>> "))
        else:
            value = input(f"\nPlease enter the phrase to remove from the {key}.\n>> ")
            if value in gvars.config[key]:
                gvars.config[key].remove(value)
            else:
                print(f"{value} is not present in the blacklist.")
                return True

    else:

        # All edits that require one integer value.        
        if choice in ["3", "4", "5", "13"]:
            value = "k"
            while True:
                value = input(f"\nEditing {key}\nPlease enter an integer value\n>> ")
                try:
                    gvars.config[key] = int(value)
                    break
                except TypeError as e:
                    print(f"{e} - Not an integer.")

        # All edits that require boolean values.
        elif choice in ["6", "8"]:
            value = "k"
            while True:
                value = input(f"\nEditing {key}\nPlease enter a boolean value\n>> ")
                try:
                    gvars.config[key] = json.loads(value.lower())
                    break
                except TypeError as e:
                    print(f"{e} - Not a boolean.")

        # All edits that require one string value.
        elif choice in ["7", "12"]:
            gvars.config[key] = input(f"\nEditing {key}\nPlease enter the new value\n>> ")

        # Replaces waitUnit
        elif choice == "11":
            print(f"Editing {key}")
            newUnit = [
                input("Please enter the singular noun for the new unit. \n>> "),
                input("Please enter the plural noun for the new unit. \n>> "),
                int(input("Please enter the numerical value of the new unit converted into seconds. \n>> "))
            ]
            gvars.config[key] = newUnit

        # Replaces int, string and bool values
        else:
            gvars.config[key] = input(f"\nEditing {key}\nPlease enter the value\n>> ")

    gvars.config.pop("cutoffSec")
    gvars.config.pop("waitTime")
    outConfig = {}
    outConfig["config"] = []
    outConfig["config"].append(gvars.config)
    with open(gvars.home+"/.oscr/config.json", "w") as outFile:
        outFile.write(json.dumps(outConfig, indent=4, sort_keys=True))

    gvars = calculateEssentials(gvars)

    return True

# No refresh token support implemented yet, but I'm preparing for it
# Does what it says on the fucking tin
def editPraw(gvars):

    # Setup results
    results = []
    resultNames = [
        "client_id",
        "client_secret",
        "username",
        "password",
        "Return to main settings menu"
        #"refresh_token"
    ]
    
    # Prints menu
    print("\nWhich option would you like?")
    for i in range(len(resultNames)):
        print(f"{i+1}. {resultNames[i]}")
        results.append(str(i+1))
    
    # Get user choice
    choice = validateChoice(results)
    key = resultNames[int(choice)-1]
    
    # Returns to main settings menu
    if choice == "5":
        return True
    
    try:
        
        # Retrieve information from praw.ini
        with open(gvars.home+"/.config/praw.ini", "r+") as file:
            content = file.read().splitlines()
            success = False
            allowChanges = False
            
            # Find and replace necessary line
            for line in content:
                if not line == "":
                    if list(line)[0] == "[" and line in ["[oscr]", "[oscr]          "]:
                        allowChanges = True
                    elif list(line)[0] == "[":
                        allowChanges = False
                    if allowChanges and not list(line[0]) == "[":
                        lineStart = line.split("=")[0]
                        if lineStart == key:
                            oldLine = line
                            line = key+"="+input(f"\nEditing {key}\nPlease enter the new value\n>> ")
                            if len(oldLine) > len(line):
                                line = line + " "*(len(oldLine)-len(line))
                            content[content.index(oldLine)] = line
                            success = True
                else:
                    doLog("Skipping irrelevant line: " + line, gvars)
            
            # Writes content back into file
            if success:
                
                # Ensure all lines have newlines at the end, because apparently writelines is loathe to do this
                for line in content:
                    content[content.index(line)] = line+"\n"
                file.seek(0)
                file.writelines(content)
            
            # In case necessary line is not found
            else:
                if key in resultNames[0:3]:
                    doLog(f"{key} is not in praw.ini.", gvars)
                #if key in [3]:
                #    print("If you are using refresh tokens to log in, please choose that option instead.")
                #    return False
                #elif key in [4]:
                #    print("If you are not using refresh tokens to log in, please choose password instead.")
                #    return False
                createIni(gvars)
    
    # In case praw.ini is not found
    except FileNotFoundError:
        doLog("praw.ini file not found.", gvars)
        createIni(gvars)

    return True
    
# Validates the user's choice to make sure it's in the viable results
# The only function in this module that doesn't look like shrek got acne
def validateChoice(results):
    choice = ""
    while choice not in results:
        choice = input("\n>> ")
        if choice not in results:
            print(f"Please enter a number from 1 to {results[len(results)-1]}.")
    return choice
