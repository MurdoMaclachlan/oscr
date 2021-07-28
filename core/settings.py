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
from typing import List, NoReturn
from .globals import Globals, Log, System
from .ini import createIni
from .log import exitWithLog, updateLog
from .misc import dumpConfig
global Globals, Log, System

# Main settings menu
# If-tree the first, but not the last
def settingsMain() -> NoReturn:

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
        choice = validateChoice(["1", "2", "3", "4", "5"])

        # Determines which result happens
        if choice == "1":
            Log.new(["Opening config edit menu."])
            editConfig()
        elif choice == "2":
            Log.new(
                [
                    "Opening praw.ini edit menu.",
                    Log.warning("WARNING: edits to praw.ini will require a restart to take effect.")
                ]
            )
            editPraw()
        elif choice == "3":
            howToUse()
        elif choice == "4":
            Log.new(["Exiting settings menu, continuing to main program."])
            break
        else:
            updateLog(["Updating log..."])
            exitWithLog(["Log updated successfully."])
            sys.exit(0)

# This fucking shite is the bane of my existence
# You'd think I wouldn't need to turn my r/badcode flair into actual fucking code
# But apparently I do
# Does what it says on the fucking tin
def editConfig() -> bool:

    # Gets user choice
    print(
        "\nWhich option would you like?"
        "\n1. Add to blacklist"
        "\n2. Remove from blacklist"
        "\n3. Case sensitive"
        "\n4. Cutoff"
        "\n5. Cutoff unit"
        "\n6. Debug"
        "\n7. Limit"
        "\n8. Log updates"
        "\n9. Operating system"
        "\n10. Print logs"
        "\n11. Recur"
        "\n12. Add to regexBlacklist"
        "\n13. Remove from regexBlacklist"
        "\n14. Add to subredditList"
        "\n15. Remove from subredditList"
        "\n16. Wait unit"
        "\n17. User"
        "\n18. Use regex"
        "\n19. Add to userList"
        "\n20. Remove from userList"
        "\n21. Wait amount"
        "\n22. Return to main settings menu"
    )
    resultNames = list(Globals.config.keys())
    choice = validateChoice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"])

    # Returns to main settings menu
    if choice == "21":
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
            "11":"9",
            "12":"10",
            "13":"10",
            "14":"11",
            "15":"11",
            "16":"12",
            "17":"13",
            "18":"14",
            "19":"15",
            "20":"15",
            "21":"16"
        }
    
    key = resultNames[int(keys[choice])]
    
    # Adds/removes from blacklist
    if choice in ["1", "2", "12", "13", "14", "15", "19", "20"]:  
  
        if choice in ["1", "12", "14", "19"]:
            value = input(f"\nPlease enter the phrase to add to the {key}\n>> ")
            if value == "-e":
                return True
            Globals.config[key].append()
        else:
            value = input(f"\nPlease enter the phrase to remove from the {key}.\n>> ")
            if value == "-e":
                return True
            if value in Globals.config[key]:
                Globals.config[key].remove(value)
            else:
                print(f"{value} is not present in the blacklist.")
                return True

    else:

        # All edits that require one integer value.        
        if choice in ["4", "5", "7", "21"]:
            while True:
                value = input(f"\nEditing {key}\nPlease enter an integer value\n>> ")
                if value == "-e":
                    return True
                try:
                    Globals.config[key] = int(value)
                    break
                except TypeError as e:
                    print(f"{e} - Not an integer.")

        # All edits that require boolean values.
        elif choice in ["3", "6", "8", "10", "18"]:
            while True:
                value = input(f"\nEditing {key}\nPlease enter a boolean value\n>> ")
                if value == "-e":
                    return True
                try:
                    Globals.config[key] = json.loads(value.lower())
                    break
                except TypeError as e:
                    print(f"{e} - Not a boolean.")

        # All edits that require one string value.
        elif choice in ["9", "17"]:
            value = input(f"\nEditing {key}\nPlease enter the new value\n>> ")
            if value == "-e":
                return True
            Globals.config[key] = value
            
        # Replaces waitUnit
        elif choice == "16":
            print(f"Editing {key}")
            newUnit = [
                input("Please enter the singular noun for the new unit. \n>> "),
                input("Please enter the plural noun for the new unit. \n>> "),
                int(input("Please enter the numerical value of the new unit converted into seconds. \n>> "))
            ]
            Globals.config[key] = newUnit

    return dumpConfig()

# No refresh token support implemented yet, but I'm preparing for it
# Does what it says on the fucking tin
def editPraw() -> bool:

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
        with open(f"{System.PATHS['config']}/praw.ini", "r+") as file:
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
                    Log.new([f"Skipping irrelevant line: {line}"])
            
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
                    Log.new([f"{key} is not in praw.ini."])
                #if key == resultNames[3]:
                #    print("If you are using refresh tokens to log in, please choose that option instead.")
                #    return False
                #elif key == resultNames[4]:
                #    print("If you are not using refresh tokens to log in, please choose password instead.")
                #    return False
                createIni()
    
    # In case praw.ini is not found
    except FileNotFoundError:
        Log.new([Log.warning("praw.ini file not found.")])
        createIni()

    return True

# Prints explanation of how to use the settings menu
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
def validateChoice(results: List) -> str:
    choice = ""
    while choice not in results:
        choice = input("\n>> ")
        if choice not in results:
            print(f"Please enter a number from 1 to {results[len(results)-1]}.")
    return choice
