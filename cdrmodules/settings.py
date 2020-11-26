# This whole module is an ugly bastard, but it works
# I'll deal with it eventually probably maybe

import sys
import json
from .log import doLog, updateLog
from .misc import calculateEssentials

# Main settings menu
# If-tree the first, but not the last
def settingsMain(gvars):

    doLog("Success: reached settings menu.", gvars)

    while True:
        # Gets user choice
        print("\nOPTIONS MENU\n1. Edit config\n2. Edit praw.ini [under construction]\n3. Continue to program\n4. Exit")
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
            updateLog("Exiting CDRemover.", gvars)
            sys.exit(0)

# This fucking shite is the bane of my existence
# you'd think I wouldn't need to turn my r/badcode flair into actual fucking code
# but apparently I do
# does what it says on the fucking tin
def editConfig(gvars):

    # Gets user choice
    print("\nWhich config option would you like to edit?\n1. Add to blacklist\n2. Remove from blacklist\n3. Cutoff\n4. Cutoff unit\n5. Limit\n6. Log updates\n7. Operating system\n8. Recur\n9. ToR only\n10. Wait unit\n11. Username\n12. Wait amount")
    results = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    resultNames = list(gvars.config.keys())
    choice = validateChoice(results)

    # All possible results 

    key = resultNames[int(choice)-2]

    # Adds/removes from blacklist
    if choice in ["1", "2"]:
  
        if choice == "1":
            key = resultNames[int(choice)-1]
            gvars.config[key].append(input("\nPlease enter the phrase to add to the blacklist.\n>> "))
        else:
            value = input("\nPlease enter the phrase to remove from the blacklist.\n>> ")
            if value in gvars.config[key]:
                gvars.config[key].remove(value)
            else:
                print(f"{value} is not present in the blacklist.")
                return True

    else:

        # All edits that require one integer value.        
        if choice in ["3", "4", "5", "12"]:
            value = "k"
            while True:
                value = input(f"\nEditing {key}\nPlease enter an integer value\n>> ")
                try:
                    gvars.config[key] = int(value)
                    break
                except TypeError as e:
                    print(f"{e} - Not an integer.")

        # All edits that require boolean values.
        elif choice in ["6", "8", "9"]:
            value = "k"
            while True:
                value = input(f"\nEditing {key}\nPlease enter a boolean value\n>> ")
                try:
                    gvars.config[key] = json.loads(value.lower())
                    break
                except TypeError as e:
                    print(f"{e} - Not a boolean.")

        # All edits that require one string value.
        elif choice in ["7", "11"]:
            gvars.config[key] = input(f"\nEditing {key}\nPlease enter the new value\n>> ")

        # Replaces waitUnit
        elif choice == "10":
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
    with open(gvars.home+"/.cdremover/config.json", "w") as outFile:
        outFile.write(json.dumps(outConfig, indent=4, sort_keys=True))

    gvars = calculateEssentials(gvars)

    return True

# Oh fuck it's editConfig 2 electric boogaloo
# does what it says on the fucking tin
def editPraw(gvars):

    print("Not ready yet.")
    return True
    
# validates the user's choice to make sure it's in the viable results
# the only function in this module that doesn't look like shrek got acne
def validateChoice(results):
    choice = ""
    while choice not in results:
        choice = input("\n>> ")
        if choice not in results:
            print(f"Please enter a number from 1 to {results[len(results)-1]}.")
    return choice
