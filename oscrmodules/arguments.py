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
from .gvars import defaultConfig, version
from .log import doLog
from .ini import reformatIni
from .misc import calculateEssentials

def checkArgs(gvars):
    
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
    passGvars = list(arguments.keys())[8:14]
    configChanges = {
        "--force-regex": [gvars, "useRegex", True],
        "-f": [gvars, "useRegex", True],
        "--no-recur": [gvars, "recur", False],
        "-n": [gvars, "recur", False],
        "--print-logs": [gvars, "printLogs", True],
        "-p": [gvars, "printLogs", True],
        "--report-totals": [gvars, "reportTotals", True],
        "-r": [gvars, "reportTotals", True]
    }
    
    # If any of the closing args, i.e. args like "help" or "version"
    # that show a specific output have been run, this flag tells it
    # not to process non-closing args and to kill the program after
    # it's done.
    closing = False
    for argument in list(arguments.keys())[0:8]:
        if argument in sys.argv:
            closing = True
    
    # Checks through all the lists to work out what to do with each arg
    for argument in arguments:
        if argument in sys.argv[1:]:
            if argument in passGvars and not closing:
                gvars = arguments[argument](gvars)
            elif argument in configChanges and not closing:
                arguments[argument](*configChanges[argument])
            elif (argument in passGvars or argument in configChanges) and closing:
                print(f"WARNING: '{argument}' was passed but was accompanied by a closing argument and will not be processed.")
            else:
                global config
                config = gvars.config
                arguments[argument]()
    
    for argument in sys.argv[1:]:
        if argument not in arguments:
            print(f"WARNING: Unknown argument '{argument}' passed - ignoring.")
    
    if closing:
        sys.exit(0)   
    
    return calculateEssentials(gvars)

"""
    Below are listed the function definitions for
    each argument.

    They functions are listed in alphabetical order
    of their names; not in alphabetical order of the
    argument name, nor in order of run-time priority.
    
    For run-time priority, see their order in the 
    'arguments' dictionary in checkArgs(), above.
"""

def formatOld(gvars):
    doLog("Reformatting CDRemover files to OSCR.", gvars)
    try:
        rename(gvars.home+"/.cdremover", gvars.home+"/.oscr")
    except FileNotFoundError: pass
    reformatIni(gvars)
    doLog("Reformatting complete.", gvars)
    return gvars

def helpMenu():
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


def printCredits():
    print(
        "\nCredits (alphabetical):\n\n"
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

def resetConfig(gvars):
    doLog("Resetting config file.", gvars)
    try:
        remove(gvars.home+"/.config/oscr/config.json")
    except FileNotFoundError:
        doLog("Config file already absent.", gvars)
    gvars.config = defaultConfig
    return gvars

def settings(gvars):
    from .settings import settingsMain
    doLog(f"Running OSCR version {version} with --settings parameter, entering settings menu.", gvars)
    gvars = settingsMain(gvars)
    return gvars

def showConfig():
    print("\nThe config is as follows:\n")
    for i in config:
        print(f"{i}: {config[i]}")

def showVersion():
    print(f"\nThe installed version of OSCR is: {version}")

def tempChangeConfig(gvars, key, val):
    gvars.config[key] = val
    return gvars
