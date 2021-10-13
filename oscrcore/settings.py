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

    Contact me at murdomaclachlan@duck.com
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
        choice = validateChoice(1,5)

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
        "\n14. Report totals"
        "\n15. Add to subredditList"
        "\n16. Remove from subredditList"
        "\n17. Wait unit"
        "\n18. User"
        "\n19. Use refresh tokens"
        "\n20. Use regex"
        "\n21. Add to userList"
        "\n22. Remove from userList"
        "\n23. Wait amount"
        "\n24. Return to main settings menu"
    )
    resultNames = list(Globals.config.keys())
    choice = validateChoice(1,j)

    # Returns to main settings menu
    if choice == "24":
        return True
    else:
        keys = {
            "1": "0",
            "2": "0",
            "3": "1",
            "4": "2",
            "5": "3",
            "6": "4",
            "7": "5",
            "8": "6",
            "9": "7",
            "10": "8",
            "11": "9",
            "12": "10",
            "13": "10",
            "14": "11",
            "15": "12",
            "16": "12",
            "17": "13",
            "18": "14",
            "19": "15",
            "20": "16",
            "21": "17",
            "22": "17",
            "23": "18"
        }
    
    key = resultNames[int(keys[choice])]
    
    # Adds/removes from blacklist
    if choice in ["1", "2", "12", "13", "15", "16", "21", "22"]:
  
        if choice in ["1", "12", "15", "21"]:
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
        if choice in ["4", "5", "7", "23"]:
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
        elif choice in ["3", "6", "8", "10", "14", "19", "20"]:
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
        elif choice in ["9", "18"]:
            value = input(f"\nEditing {key}\nPlease enter the new value\n>> ")
            if value == "-e":
                return True
            Globals.config[key] = value
            
        # Replaces waitUnit
        elif choice == "17":
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

    try:
        creds = getCredentials()
    except FileNotFoundError:
        Log.new([Log.warning(f"ERROR: file '{System.PATHS['config']}/praw.ini' not found.")])
        createIni()

    keys = creds.keys()

    # Prints menu
    print("\nWhich option would you like?")

    j = 1
    for i in keys:
        print(f"{j}. {i}")
        j += 1

    # Get user choice
    choice = validateChoice(1,j)

    key = ini[int(choice)-1]
    value = input(f"Editing {key}. Please input a new value.\n >> ")

    # Returns to the main settings menu
    if value == "-e":
        pass
    else:
        ini[key] = value
        dumpIni()

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
def validateChoice(low: int, high: int) -> str:
    results = [f"{i}" for i in range(low,high+1)]
    results.append("-e")
    choice = input("\n>> ")
    while choice not in results:
        print(f"Please enter a number from 1 to {results[len(results)-2]}.")
        choice = input("\n>> ")
    return choice
