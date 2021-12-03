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

    ----------

    This whole module is an ugly bastard, but it works. I'll deal with
    it eventually, probably, maybe...
"""

import sys
import json
from typing import List, NoReturn
from .classes import Globals, Log, System
from .creds import create_ini, get_credentials
from .log import exit_with_log, update_log
from .misc import dump_config
global Globals, Log, System


def settings_main() -> NoReturn:
    """The main settings menu; controls all other sub-menus.

    No arguments.

    No return value.
    """
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
        choice = validate_choice(1,5)

        # Determines which result happens
        if choice == "1":
            Log.new(["Opening config edit menu."])
            edit_config()
        elif choice == "2":
            Log.new(
                [
                    "Opening praw.ini edit menu.",
                    Log.warning("WARNING: edits to praw.ini will require a restart to take effect.")
                ]
            )
            edit_credentials()
        elif choice == "3":
            how_to_use()
        elif choice == "4":
            Log.new(["Exiting settings menu, continuing to main program."])
            break
        else:
            update_log(["Updating log..."])
            exit_with_log(["Log updated successfully."])
            sys.exit(0)


def edit_config() -> bool:
    """Constructs the edit config menu and deals with whichever option the user chooses.
    Should really be split into multiple methods, but I haven't got round to it yet.

    No arguments.

    Returns: boolean success status
    """
    print("\nWhich option would you like?")
    j = 1
    keys = {}

    # Iterate every config key
    for i in Globals.config.keys():
        is_list = type(Globals.config[i]) is list

        # Account for the special case and the normal cases
        if i == "unit" or not is_list:
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
        keys[f"{j}"] = f"{i}:add" if is_list else f"{i}"
        j += 1 if i == "unit" or not is_list else 2

    # Final option doesn't conform to a config key
    print(f"{j}. Return to main settings menu.")

    choice = validate_choice(1,j)

    # Returns to main settings menu
    if choice == f"{j+1}": return True

    target = keys[choice].split(":")[0]

    print(f"\nEditing '{target}'. Current value: '{Globals.config[target]}'")

    # Adds/removes from blacklist
    if type(Globals.config[target]) is list and target != "unit":
        mode = keys[choice].split(":")[1]
        value = input(f"Please enter the phrase to {mode} {('from', 'to')[mode == 'add']} the {target}\n>> ")

        if value == "-e":
            return True

        if mode == "add":
            Globals.config[target].append(value)
        else:
            if value in Globals.config[target]:
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
        new_unit = [
            input("Please enter the singular noun for the new unit. \n>> "),
            input("Please enter the plural noun for the new unit. \n>> "),
            int(input("Please enter the numerical value of the new unit converted into seconds. \n>> "))
        ]
        Globals.config[target] = new_unit

    return dump_config()


def edit_credentials() -> bool:
    """Provides a menu for selecting and editing Reddit credentials. Upon a successful
    edit, will output updated credentials to praw.ini.

    No arguments.

    Returns: boolean success status.
    """
    try:
        creds = get_credentials()
    except FileNotFoundError:
        Log.new(
            Log.warning(f"ERROR: file '{System.PATHS['config']}/praw.ini' not found.")
        )
        if create_ini():
            creds = get_credentials()
        else:
            return False

    keys = creds.keys()

    # Prints menu
    print("\nWhich option would you like?")

    j = 1
    for i in keys:
        print(f"{j}. {i}")
        j += 1

    # Get user choice
    choice = validate_choice(1,j)

    key = creds[int(choice)-1]
    value = input(f"Editing {key}. Please input a new value.\n >> ")

    # Returns to the main settings menu
    if value == "-e":
        pass
    else:
        creds[key] = value
        dump_credentials(creds)

    return True


def how_to_use():
    """Prints guide for using the settings menu.

    No arguments.

    No return value.
    """
    print(
        "\nHOW TO USE\n",
        "This menu is designed for editing the config file and the praw.ini file for this program.\n",
        "You enter numbers to select a menu, and can from there select specific keys to change the values of.\n",
        "Currently, you cannot change existing entries in lists, and would have to remove and re-add them to modify them.\n",
        "If you accidentally select a key you did not mean to, you are not required to close the program;\n",
        "simply entering '-e' will return you to the main settings menu."
    )
    input("\nPress enter to return to the main settings menu.")


def validate_choice(low: int, high: int) -> str:
    """Validates the user's choice based on a list generated from a given range of
    numbers.

    Arguments:
    - low (int)
    - high (int)

    Returns: a single numerical string.
    """
    results = [f"{i}" for i in range(low,high+1)]
    results.append("-e")
    choice = input("\n>> ")
    while choice not in results:
        print(f"Please enter a number from 1 to {results[len(results)-2]}.")
        choice = input("\n>> ")
    return choice
