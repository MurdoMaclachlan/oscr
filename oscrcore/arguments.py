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

    This module handles functions relating to the identification and
    processing of run-time arguments passed to the OSCR script.
"""

import sys
from os import remove
from typing import Any, List, NoReturn
from .classes import Globals, Log, System
from .misc import calculate_essentials, dump_config
global Globals, Log, System


def check_args() -> NoReturn:
    """Checks all passed arguments against a master list, processes them in the right
    order and calls the necessary functions.

    No arguments.

    No return value.
    """
    # Setting up of essential dicts and lists
    arguments = {
        "--help": help_menu,  # priority 1
        "-h": help_menu,
        "--version": show_version,  # priority 2
        "-v": show_version,
        "--credits": print_credits,  # priority 3
        "-c": print_credits,
        "--show-config": show_config,  # priority 4
        "-s": show_config,
        "--reset-config": reset_config,  # priority 5
        "-R": reset_config,
        "--settings": settings,  # priority 6
        "-S": settings,
        "--force-regex": temp_config_change,  # lowest priority; alphabetical
        "-f": temp_config_change,
        "--clean-hunt": clean_hunt,
        "-C": clean_hunt,
        "--no-recur": temp_config_change,
        "-n": temp_config_change,
        "--print-logs": temp_config_change,
        "-p": temp_config_change,
        "--report-totals": temp_config_change,
        "-r": temp_config_change
    }
    
    # List of argumets that require a change to the config
    config_changes = {
        "--force-regex": [["use_regex", True]],
        "-f": [["use_regex", True]],
        "--no-recur": [["recur", False]],
        "-n": [["recur", False]],
        "--print-logs": [["print_logs", True]],
        "-p": [["print_logs", True]],
        "--report-totals": [["report_totals", True]],
        "-r": [["report_totals", True]],
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
            if not closing and argument in config_changes:
                arguments[argument](config_changes[argument])
                if argument in ["--clean-hunt", "-C"] and sys.argv.index(argument) != len(sys.argv):
                    print(Log.warning("WARNING: --clean-hunt was passed, but so were other arguments. Subsequent arguments will not be processed."))
            
            # If a closing argument and an argument that will be overwritten by it were both passed, warns user
            elif (argument in list(arguments.keys())[8:] or argument in config_changes) and closing:
                print(Log.warning(f"WARNING: '{argument}' was passed but was accompanied by a closing argument and will not be processed."))
            
            else:
                arguments[argument]()
    
    # Handles passing of unknown arguments
    for argument in sys.argv[1:]:
        if argument not in arguments:
            print(Log.warning(f"WARNING: Unknown argument '{argument}' passed - ignoring.", Globals))
    
    sys.exit(0) if closing else calculate_essentials()


"""
    Below are listed the function definitions for
    each argument.

    They functions are listed in alphabetical order
    of their names; not in alphabetical order of the
    argument name, nor in order of run-time priority.
    
    For run-time priority, see their order in the
    'arguments' dictionary in checkArgs(), above.
"""


def clean_hunt() -> NoReturn:
    """Performs the necessary temporary configuration changes for the --client-hunt
    runtime mode.

    No arguments.

    No return value.
    """
    # I'm going to clean this shit up in 2.1.0
    # lol nvm I'll do it 2.2.0
    temp_config_change([
        ["regex_blacklist", ["^(claim|claiming|done).*treasure *hunt.*"]] if Globals.get(key="use_regex") else ["blacklist", ["claim -- treasure hunt", "done -- treasure hunt"]],
        ["recur", False],
        ["", ""] if Globals.get(key="user_list") == ["transcribersofreddit"] else ["user_list", ["transcribersofreddit"]]
    ])

    
def help_menu() -> NoReturn:
    """Prints a list of arguments and their functionalities.

    No arguments.

    No return value.
    """
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


def print_credits() -> NoReturn:
    """Prints a list of contributors, what they have contributed, and links to various
    accounts or websites of theirs.

    No arguments.

    No return value.
    """
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


def reset_config() -> NoReturn:
    """Deletes the config file and replaces it with the default config; prompts for
    username before saving the default.

    No arguments.

    No return value.
    """
    Log.new(["Resetting config file."])
    try:
        remove(f"{System.PATHS['config']}/config.json")
    except FileNotFoundError:
        Log.new(["Config file already absent."])
    Globals.set(Globals.DEFAULT_CONFIG)
    Globals.set(input("Please enter your Reddit username:\n  /u/"), key="user")
    dump_config()


def settings() -> NoReturn:
    """Enters the settings menu.

    No arguments.

    No return value.
    """
    from .settings import settings_main
    Log.new(["Running OSCR with --settings parameter, entering settings menu."])
    settings_main()


def show_config() -> NoReturn:
    """Prints the contents of the config file.

    No arguments.

    No return value.
    """
    print("The config is as follows:\n")
    config = Globals.get()
    for i in config:
        print(f"{i}: {config[i]}")


def show_version() -> NoReturn:
    """Prints the current version number.

    No arguments.

    No return value.
    """
    print(f"The installed version of OSCR is: {Globals.VERSION}")


def temp_config_change(keys: List[List[Any]]) -> NoReturn:
    """Executes a list of config changes.

    Arguments:
    - keys (array of arrays)

    No return value.
    """
    for key in keys:
        # This check allows for dynamic construction of passed lists
        if key == ["", ""]: continue
        else: Globals.set(key[1], key=key[0])
