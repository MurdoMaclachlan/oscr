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

import sys
from os import remove, rename
from typing import NoReturn
from .globals import defaultConfig, VERSION
from .log import doLog, warn
from .ini import reformatIni
from .misc import calculateEssentials

def checkArgs(Globals: object) -> object:
    
    # Setting up of essential dicts and lists
    arguments = {
        "--help": helpMenu, # priority 1
        "-h": helpMenu,
        "--version": showVersion, # priority 2
        "-v": showVersion,
        "--credits": printCredits, # priority 3
        "-c": printCredits,
        "--show-config": showConfig, # priority 4
        "-s": showConfig,
        "--format-old": formatOld, # priority 5
        "-F": formatOld,
        "--reset-config": resetConfig, # priority 6
        "-R": resetConfig,
        "--settings": settings, # priority 7
        "-S": settings,
        "--force-regex": tempChangeConfig, # lowest priority; alphabetical
        "-f": tempChangeConfig,
        "--no-recur": tempChangeConfig,
        "-n": tempChangeConfig,
        "--print-logs": tempChangeConfig,
        "-p": tempChangeConfig,
        "--report-totals": tempChangeConfig,
        "-r": tempChangeConfig
    }
    passGlobals = list(arguments.keys())[8:14]
    configChanges = {
        "--force-regex": [Globals, "useRegex", True],
        "-f": [Globals, "useRegex", True],
        "--no-recur": [Globals, "recur", False],
        "-n": [Globals, "recur", False],
        "--print-logs": [Globals, "printLogs", True],
        "-p": [Globals, "printLogs", True],
        "--report-totals": [Globals, "reportTotals", True],
        "-r": [Globals, "reportTotals", True]
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
            if argument in passGlobals and not closing:
                Globals = arguments[argument](Globals)
            elif argument in configChanges and not closing:
                arguments[argument](*configChanges[argument])
            elif (argument in passGlobals or argument in configChanges) and closing:
                print(warn(f"WARNING: '{argument}' was passed but was accompanied by a closing argument and will not be processed.", Globals))
            else:
                global config
                config = Globals.config
                arguments[argument]()
    
    for argument in sys.argv[1:]:
        if argument not in arguments:
            print(warn(f"WARNING: Unknown argument '{argument}' passed - ignoring.", Globals))
    
    if closing:
        sys.exit(0)   
    
    return calculateEssentials(Globals)

"""
    Below are listed the function definitions for
    each argument.

    They functions are listed in alphabetical order
    of their names; not in alphabetical order of the
    argument name, nor in order of run-time priority.
    
    For run-time priority, see their order in the 
    'arguments' dictionary in checkArgs(), above.
"""

def formatOld(Globals: object) -> object:
    doLog(["Reformatting CDRemover files to OSCR."], Globals)
    try:
        rename(Globals.HOME+"/.cdremover", Globals.HOME+"/.oscr")
    except FileNotFoundError: pass
    reformatIni(Globals)
    doLog(["Reformatting complete."], Globals)
    return Globals

def helpMenu() -> NoReturn:
    print(
        "List of Arguments:\n",
        "--credits, -c:       lists everyone who has helped with the creation of the program\n",
        "--force-regex, -f:   forces the program to enable regex for one instance regardless of configuration\n",
        "--format-old, -F:    rename old .cdremover directories, etc. to fit OSCR's new name, and move old praw.ini to new location\n",
        "--help, -h:          displays this list\n",
        "--no-recur, -n:      forces program to run only one cycle regardless of 'recur' configuration\n",
        "--print-logs, -p:    forces program to print logs for one instance regardless of 'printLogs' configuration\n",
        "--reset-config, -R:  resets the config file to defaults\n",
        "--report-totals, -r: forces program to report total statistics for one instance regardless of 'reportTotals' configuration\n",
        "--settings, -S:      runs the settings menu\n",
        "--show-config, -s:   displays the contents of the config file\n",
        "--version, -v:       displays the currently installed version"
    )


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

def resetConfig(Globals: object) -> object:
    doLog(["Resetting config file."], Globals)
    try:
        remove(Globals.HOME+"/.config/oscr/config.json")
    except FileNotFoundError:
        doLog(["Config file already absent."], Globals)
    Globals.config = defaultConfig
    return Globals

def settings(Globals: object) -> object:
    from .settings import settingsMain
    doLog([f"Running OSCR version {VERSION} with --settings parameter, entering settings menu."], Globals)
    return settingsMain(Globals)

def showConfig() -> NoReturn:
    print("The config is as follows:\n")
    for i in config:
        print(f"{i}: {config[i]}")

def showVersion() -> NoReturn:
    print(f"The installed version of OSCR is: {VERSION}")

def tempChangeConfig(Globals: object, key: str, val: bool) -> object:
    Globals.config[key] = val
    return Globals
