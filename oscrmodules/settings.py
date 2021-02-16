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
from .misc import calculateEssentials, createIni, tryDumpConfig

# Main settings menu
# If-tree the first, but not the last
def settingsMain(gvars):

    doLog("Success: reached settings menu.", gvars)

    while True:
        # Gets user choice
        print(
            "\nOPTIONS MENU"
            "\n1. Edit config"
            "\n2. Edit praw.ini"
            "\n3. How to use this menu"
            "\n4. Continue to program"
            "\n5. Exit"
        )
        results = ["1", "2", "3", "4", "5"]
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
            howToUse()
        elif choice == "4":
            gvars = calculateEssentials(gvars)
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
    print(
        "\nWhich option would you like?"
        "\n1. Add to blacklist"
        "\n2. Remove from blacklist"
        "\n3. Case sensitive"
        "\n4. Cutoff"
        "\n5. Cutoff unit"
        "\n6. Limit"
        "\n7. Log updates"
        "\n8. Operating system"
        "\n9. Recur"
        "\n10. Add to regexBlacklist"
        "\n11. Remove from regexBlacklist"
        "\n12. Add to subredditList"
        "\n13. Remove from subredditList"
        "\n14. Wait unit"
        "\n15. Use regex"
        "\n16. User"
        "\n17. Wait amount"
        "\n18. Return to main settings menu"
    )
    results = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
    resultNames = list(gvars.config.keys())
    choice = validateChoice(results)

    # Returns to main settings menu
    if choice == "18":
        return True
    else:
        keys = {
            "1":"0",
            "2":"0",
            "3":"1",
            "4":"2",
            "5":"3",
            "6":"4",
            "7":"5",
            "8":"6",
            "9":"7",
            "10":"8",
            "11":"8",
            "12":"9",
            "13":"9",
            "14":"10",
            "15":"11",
            "16":"12",
            "17":"13",
        }
    
    key = resultNames[int(keys[choice])]
    
    # Adds/removes from blacklist
    if choice in ["1", "2", "10", "11", "12", "13"]:  
  
        if choice in ["1", "10", "12"]:
            value = input(f"\nPlease enter the phrase to add to the {key}\n>> ")
            if value == "-e":
                return True
            gvars.config[key].append()
        else:
            value = input(f"\nPlease enter the phrase to remove from the {key}.\n>> ")
            if value == "-e":
                return True
            if value in gvars.config[key]:
                gvars.config[key].remove(value)
            else:
                print(f"{value} is not present in the blacklist.")
                return True

    else:

        # All edits that require one integer value.        
        if choice in ["4", "5", "6", "17"]:
            while True:
                value = input(f"\nEditing {key}\nPlease enter an integer value\n>> ")
                if value == "-e":
                    return True
                try:
                    gvars.config[key] = int(value)
                    break
                except TypeError as e:
                    print(f"{e} - Not an integer.")

        # All edits that require boolean values.
        elif choice in ["3", "7", "9", "15"]:
            while True:
                value = input(f"\nEditing {key}\nPlease enter a boolean value\n>> ")
                if value == "-e":
                    return True
                try:
                    gvars.config[key] = json.loads(value.lower())
                    break
                except TypeError as e:
                    print(f"{e} - Not a boolean.")

        # All edits that require one string value.
        elif choice in ["8", "16"]:
            value = input(f"\nEditing {key}\nPlease enter the new value\n>> ")
            if value == "-e":
                return True
            gvars.config[key] = value
            
        # Replaces waitUnit
        elif choice == "14":
            print(f"Editing {key}")
            newUnit = [
                input("Please enter the singular noun for the new unit. \n>> "),
                input("Please enter the plural noun for the new unit. \n>> "),
                int(input("Please enter the numerical value of the new unit converted into seconds. \n>> "))
            ]
            gvars.config[key] = newUnit

    tryDumpConfig(gvars)    

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
        #"refresh_token",
        "Return to main settings menu"
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
                    if line in ["[oscr]", "[oscr]          "]:
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
                #if key == resultNames[3]:
                #    print("If you are using refresh tokens to log in, please choose that option instead.")
                #    return False
                #elif key == resultNames[4]:
                #    print("If you are not using refresh tokens to log in, please choose password instead.")
                #    return False
                createIni(gvars)
    
    # In case praw.ini is not found
    except FileNotFoundError:
        doLog("praw.ini file not found.", gvars)
        createIni(gvars)

    return True
    
def howToUse():
    print(
        "\nHOW TO USE\n",
        "This menu is designed for editing the config file and the praw.ini file for this program.\n",
        "You enter numbers to select a menu, and can from there select specific keys to change the values of.\n",
        "Currently, you cannot change existing entries in lists, and would have to remove and re-add them to modify them.\n",
        "If you accidentally select a key you did not mean to, you are not required to close the program;\n",
        "simply entering '-e' will return you to the main settings menu."
    )
    input("\nPress enter to return to the main settings menu.")

# Validates the user's choice to make sure it's in the viable results
# The only function in this module that doesn't look like shrek got acne
def validateChoice(results):
    choice = ""
    while choice not in results:
        choice = input("\n>> ")
        if choice not in results:
            print(f"Please enter a number from 1 to {results[len(results)-1]}.")
    return choice
