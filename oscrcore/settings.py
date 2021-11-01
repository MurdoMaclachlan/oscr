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

    print("\nWhich option would you like?")
    j = 1
    keys = {}

    # Iterate every config key
    for i in Globals.config.keys():
        isList = type(Globals.config[i]) is list

        # Account for the special case and the normal cases
        if i == "unit" or not isList:
            print(f"{j}. {i}")

        # If the config is a list, add options for both addition and removal
        else:
            print(
                f"{j}. Add to {i}"
                f"\n{j+1}. Remove from {i}"
            )

            # Add extra key since the array is listed twice in the options
            keys[f"{j+1}"] = f"{i}:remove"

        # Add key, increment counter by appropriate amount
        keys[f"{j}"] = f"{i}:add" if isList else f"{i}"
        j += 1 if i == "unit" or not isList else 2

    # Final option doesn't conform to a config key
    print(f"{j}. Return to main settings menu.")

    choice = validateChoice(1,j)

    # Returns to main settings menu
    if choice == f"{j+1}": return True

    target = keys[choice].split(":")[0]

    print(f"\nEditing '{target}'. Current value: '{Globals.config[target]}'")

    # Adds/removes from blacklist
    if type(Globals.config[target]) is list and target != "unit":
        mode = keys[choice].split(":")[1]
        value = input(f"Please enter the phrase to {mode} {('from', 'to')[mode == 'add']} the {key}\n>> ")

        if value == "-e":
            return True

        if mode == "add":
            Globals.config[target].append(value)
        else:
            if value in Globals.config[key]:
                Globals.config[target].remove(value)
            else:
                print(f"{value} is not present in the blacklist.")
                return True

    # All edits that require integer values.
    elif type(Globals.config[target]) is int:
        while True:
            value = input("Please enter an integer value\n>> ")
            if value == "-e":
                return True
            try:
                Globals.config[target] = int(value)
                break
            except TypeError as e:
                print(f"{e} - Not an integer.")

    # All edits that require boolean values.
    elif type(Globals.config[target]) is bool:
        while True:
            value = input("Please enter a boolean value\n>> ")
            if value == "-e":
                return True
            try:
                Globals.config[target] = json.loads(value.lower())
                break
            except TypeError as e:
                print(f"{e} - Not a boolean.")

    # All edits that require one string value.
    elif type(Globals.config[target]) is str:
        value = input("Please enter the new value\n>> ")
        if value == "-e":
            return True
        Globals.config[target] = value

    # Special child
    elif target == "unit":
        newUnit = [
            input("Please enter the singular noun for the new unit. \n>> "),
            input("Please enter the plural noun for the new unit. \n>> "),
            int(input("Please enter the numerical value of the new unit converted into seconds. \n>> "))
        ]
        Globals.config[target] = newUnit

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

    key = creds[int(choice)-1]
    value = input(f"Editing {key}. Please input a new value.\n >> ")

    # Returns to the main settings menu
    if value == "-e":
        pass
    else:
        creds[key] = value
        dumpCredentials()

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
