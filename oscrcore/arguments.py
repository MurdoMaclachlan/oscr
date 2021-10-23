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

import sys
from os import remove
from typing import Any, List, NoReturn
from .globals import DEFAULT_CONFIG, Globals, Log, System
from .misc import calculateEssentials, dumpConfig
global Globals, Log, System


def checkArgs() -> NoReturn:
    
    # Setting up of essential dicts and lists
    arguments = {
        "--help": helpMenu,  # priority 1
        "-h": helpMenu,
        "--version": showVersion,  # priority 2
        "-v": showVersion,
        "--credits": printCredits,  # priority 3
        "-c": printCredits,
        "--show-config": showConfig,  # priority 4
        "-s": showConfig,
        "--reset-config": resetConfig,  # priority 5
        "-R": resetConfig,
        "--settings": settings,  # priority 6
        "-S": settings,
        "--force-regex": tempChangeConfig,  # lowest priority; alphabetical
        "-f": tempChangeConfig,
        "--clean-hunt": cleanHunt,
        "-C": cleanHunt,
        "--no-recur": tempChangeConfig,
        "-n": tempChangeConfig,
        "--print-logs": tempChangeConfig,
        "-p": tempChangeConfig,
        "--report-totals": tempChangeConfig,
        "-r": tempChangeConfig
    }
    
    # List of argumets that require a change to the config
    configChanges = {
        "--force-regex": [["useRegex", True]],
        "-f": [["useRegex", True]],
        "--no-recur": [["recur", False]],
        "-n": [["recur", False]],
        "--print-logs": [["printLogs", True]],
        "-p": [["printLogs", True]],
        "--report-totals": [["reportTotals", True]],
        "-r": [["reportTotals", True]]
    }
    
    # If any of the closing args, i.e. args like "help" or "version"
    # that show a specific output have been run, this flag tells it
    # not to process non-closing args and to kill the program after
    # it's done.
    closing = False
    for argument in list(arguments.keys())[:8]:
        if argument in sys.argv:
            closing = True
    
    # Checks through all the lists to work out what to do with each arg
    for argument in arguments:
        if argument in sys.argv[1:]:
            
            # If argument changes config and is not closing, will call its appropriate function
            if not closing and argument in configChanges:
                arguments[argument](configChanges[argument])
                if argument in ["--clean-hunt", "-C"] and sys.argv.index(argument) != len(sys.argv):
                    print(Log.warning("WARNING: --clean-hunt was passed, but so were other arguments. Subsequent arguments will not be processed."))
            
            # If a closing argument and an argument that will be overwritten by it were both passed, warns user
            elif (argument in list(arguments.keys())[8:] or argument in configChanges) and closing:
                print(Log.warning(f"WARNING: '{argument}' was passed but was accompanied by a closing argument and will not be processed."))
            
            else:
                arguments[argument]()
    
    # Handles passing of unknown arguments
    for argument in sys.argv[1:]:
        if argument not in arguments:
            print(Log.warning(f"WARNING: Unknown argument '{argument}' passed - ignoring.", Globals))
    
    sys.exit(0) if closing else calculateEssentials()


"""
    Below are listed the function definitions for
    each argument.

    They functions are listed in alphabetical order
    of their names; not in alphabetical order of the
    argument name, nor in order of run-time priority.
    
    For run-time priority, see their order in the
    'arguments' dictionary in checkArgs(), above.
"""


# Performs necessary configuration changes for --clean-hunt runtime arg
def cleanHunt() -> NoReturn:
    
    # I'm going to clean this shit up in 2.1.0
    tempChangeConfig([
        ["regexBlacklist", ["^(claim|claiming|done).*treasure *hunt.*"]] if Globals.config["useRegex"] else ["blacklist", ["claim -- treasure hunt", "done -- treasure hunt"]],
        ["recur", False],
        ["", ""] if Globals.config["userList"] == ["transcribersofreddit"] else ["userList", ["transcribersofreddit"]]
    ])


# Prints a list of arguments and their functions
def helpMenu() -> NoReturn:
    print(
        "List of Arguments:\n",
        "--clean-hunt, -C:    runs an isolated instance of OSCR that deletes ToR bot interactions containing the phrase 'treasure hunt'\n",
        "--credits, -c:       lists everyone who has helped with the creation of the program\n",
        "--force-regex, -f:   forces the program to enable regex for one instance regardless of configuration\n",
        "--help, -h:          displays this list\n",
        "--no-recur, -n:      forces program to run only one cycle regardless of 'recur' configuration\n",
        "--print-logs, -p:    forces program to print logs for one instance regardless of 'printLogs' configuration\n",
        "--reset-config, -R:  resets the config file to defaults\n",
        "--report-totals, -r: forces program to report total statistics for one instance regardless of 'reportTotals' configuration\n",
        "--settings, -S:      runs the settings menu\n",
        "--show-config, -s:   displays the contents of the config file\n",
        "--version, -v:       displays the currently installed version"
    )


# Prints a list of contributors and their contributions
def printCredits() -> NoReturn:
    print(
        "Credits (alphabetical):\n\n"
        "/u/--B_L_A_N_K--\n",
        "GitHub: https://github.com/BLANK-TH/ \n",
        "Reddit: https://www.reddit.com/user/--B_L_A_N_K--/ \n",
        "Twitch: https://www.twitch.tv/BLANK_DvTH/ \n",
        "- Real-time deletion\n",
        "- Improved output formatting\n",
        "- Help with Windows compatibility\n\n"
        "/u/DasherPack\n",
        "Reddit: https://www.reddit.com/user/DasherPack/ \n",
        "- Being a handsome boi\n\n"
        "/u/metaquarx\n",
        "GitHub: https://github.com/metaquarx/\n",
        "Reddit: https://www.reddit.com/u/metaquarx/\n",
        "Twitch: https://www.twitch.tv/metaquarx/\n",
        "- Help with regex support\n\n"
        "/u/MurdoMaclachlan\n",
        "GitHub: https://github.com/MurdoMaclachlan/\n",
        "Reddit: https://www.reddit.com/user/MurdoMaclachlan/\n",
        "Twitch: https://www.twitch.tv/murdomaclachlan/\n",
        "- Original creator and primary maintainer\n\n"
        "/u/Tim3303\n",
        "GitHub: https://github.com/TimJentzsch/\n",
        "Reddit: http://reddit.com/u/Tim3303/\n",
        "- Help with default regex list"
    )


# Deletes the config file and replaces it with the default config
# Prompts for username, then saves default config
def resetConfig() -> NoReturn:
    Log.new(["Resetting config file."])
    try:
        remove(f"{System.PATHS['config']}/config.json")
    except FileNotFoundError:
        Log.new(["Config file already absent."])
    Globals.config = DEFAULT_CONFIG
    Globals.config["user"] = input("Please enter your Reddit username:\n  /u/")
    dumpConfig()


# Enters the settings menu
def settings() -> NoReturn:
    from .settings import settingsMain
    Log.new(["Running OSCR with --settings parameter, entering settings menu."])
    settingsMain()


# Prints the contents of the config file
def showConfig() -> NoReturn:
    print("The config is as follows:\n")
    for i in Globals.config:
        print(f"{i}: {Globals.config[i]}")


# Prints the current version number
def showVersion() -> NoReturn:
    print(f"The installed version of OSCR is: {Globals.VERSION}")


# Executes a list of passed config changes
def tempChangeConfig(keys: List[List[Any]]) -> NoReturn:
    for key in keys:
        # This check allows for dynamic construction of passed lists
        if key == ["", ""]: continue
        else: Globals.editConfig(key[0], key[1])
