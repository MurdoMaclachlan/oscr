Changelogs
==========

A list of changelogs for OSCR, with the most recent version first. These are also available `here <https://github.com/MurdoMaclachlan/oscr/releases>`_.

2.1.1 - Current Release
-----------------------

**Bug Fixes**

- Fixed a crash when using regexes due to a type mismatch in the ``checkRegex()`` method.
- Fixed a crash on attempting to handle AttributeErrors in comment checking due to not specifying a dataset to call from.
- Fixed a crash on attempting to dumpStats due to an attribute naming mismatch.

2.1.0 - Current Release
-----------------------

**Functionality**

- Added refresh token support. (#33, #139)
- Added "dibs" to the default blacklist and regexBlacklist. (#140, #141)
- Removed ``--format-old`` runtime argument. (#105, #131)

**Cleanup/Optimisation**

- Deferred various functionalities in ``main.py`` to functions in other modules. (#128, #145)
- Optimised the settings menu to allow for easier addition of new config and ini options. (#127, #139, #142)
- Combined ``Log.clear()`` and ``Log.get()`` into ``Log.request()``. (#125, #130)
- Other general cleanup, readability and optimisation improvements. (#136, #137, #139, #142, #145)

**Documentation/Logs**

- Changed "core" folder to "oscrcore" to avoid issues with pip. (#138, #139)

**Bug Fixes**

- Fixed a crash on calling ``resetConfig()``. (#132, #134)
- Fixed a crash on passing an unknown run-time argument. (#133, #135)

2.0.0
-----

**Functionality**

- Added ``--clean-hunt`` runtime argument to remove comments containing "treasure hunt". (#48, #87, #115)
- Added caseSensitive config key. Determines whether or not OSCR is case sensitive when matching regexes or blacklisted comments. Set to False by default. (#57, #69)
- Added printLogs config key and ``--print-logs`` runtime argument to override the config. Determines whether or not OSCR prints the log to the console. (#70, #71)
- Added reportTotals config key and ``--report-totals`` runtime argument to override the config. Determines whether or not OSCR prints total statistics to the console. (#65, #72)
- Added "unclaiming" to the default blacklist. (#69, nice)
- OSCR now ignores punctuation when matching comments to blacklist entries. (#80, #83)
- Added userList config key. If any users are specified in the list, OSCR will only check comments that are in reply to those users. (#85, #87)
- Added ability to leave subredditList (and new userList key) empty, which will disable them, letting OSCR check comments on any subreddit or in reply to any user.
- OSCR now collects global variables at program initialisation (in the ``oscr`` script) and not ``main.py``. (#49, #75)
- Contained all code in ``main.py`` within an ``oscr()`` function for the purpose of the above change. (#50, #75)

**Cleanup/Optimisation**

- Refactored entire program with a much stronger object-oriented focus. This opens the door for a lot of backend improvements and optimisation. (#108, #109)
- Re-wrote stats handling to use JSON and classes, making ``statistics.py`` a much neater module. (#106, #109)
- Moved arguments checking to its own module, ``arguments.py``. (#52, #75)
- Moved comment handling to its own module, ``comment.py``. (#81, #82)
- Added type hinting. (#101, #103)
- Staticised constant variables. (#97, #96, #98)
- Optimised generation of ``config.json`` and ``praw.ini``. (#51, #66, #67)
- Optimised handling of ``praw.ini``, including updating & formatting from CDRemover to OSCR. (#76, #84)
- ``calculateEssentials()`` is no longer called unnecessarily. (#53, #59)
- Combined default regexBlacklist items into one regex. (#117, #118)
- Moved the default config variable to ``globals.py``. (#56, #66)
- Made many miscellaneous optimisation and readability improvements. (#77, #78, #79, #84, #96, #104, #109, #112, #114, #118, #120, #121)

**Dependencies**

- Added colored for coloured console output. (#94)
- Updated Python requirement to >= 3.5 for type hinting. (#107)

**Documentation/Logs**

- Moved documentation to readthedocs. (#93, #99)
- Renamed ``oscrmodules`` to ``core``. (#110, #111)
- Moved ``config.json`` to ``~/.config/oscr`` on Linux and Mac, and ``AppData\\Roaming\\oscr`` on Windows. (#54, #64)
- Changed how ``praw.ini`` is read and moved file to ``~/.config/oscr`` on Linux and Mac, and ``AppData\\Roaming\\oscr`` on Windows. (#55, #84)
- Improved log output surrounding comment retrieval & checking. (#60, #68)
- Added license specification to ``setup.py``. (#73, #74)
- Changed config guide from bullet point list to table. (#83)
- Added colouring to logs, currently only on warnings. (#91, #94)
- Generally improved log handling. (#95, #96)
- Renamed ``gvars`` to ``Globals``. (#100, #102)

**Bug Fixes**

- Fixed a crash on attempting to use ``--show-config`` due to accidentally assigning ``Globals()`` instance to ``gvars.config``. (#45, #58)
- Fixed an infinite loop on attempting to update integer or boolean keys in the settings menu. (#61 #63)
- Fxied regexes sometimes deleting comments that are not bot interactions. (#86, #87)
- Fixed run-time arguments not being processed in the correct priority order. (#88, #90)
- Fixed a crash on passing conflicting run-time arguments. (#89, #90)
- Fixed a potential crash on failing to update a statistic. (#92, #94)

1.2.1
-----

**Functionality**

- Added ``--version`` run-time option to print the currently installed version to the console.

**Cleanup/Optimisation**

- Minor optimisation improvements in log.py, misc.py and statistics.py.
- update() now uses smaller None-type instead of needlessly initialising an empty array.
- Removed debug time.sleep() statement from comment checker.

**Dependencies**

- praw; require >= 7.1.2.
- alive_progress; require >= 1.6.1.

**Documentation/Logs**

- Removed credits from start of main.py.

**Bug Fixes**

- #16: Recursion error on initialising Reddit instance with empty Redditor. (fixed upstream in PRAW 7.1.1)


1.2.0
-----

**Functionality**

- Added support for regexes (thanks to /u/metaquarx and /u/Tim3303 for helping with this).
- Added regex config key that tells the program whether or not to check comments using regexes, by default set to False.
- Added regexBlacklist config key, to contain the regexes to check comments against, by default excludes anything with "treasure hunt".
- Added new subredditList config key, containing a whitelist of subreddits the program is allowed to search through; contains only "transcribersofreddit" by default.
- Removed torOnly config key as of above change.
- Added a '-e' option to the settings menu, allowing users to escape to the main menu if they accidentally chose the incorrect key.
- Added a ``--show-config`` run-time option to print the contents of the config file to the console.
- Added a ``--credits`` run-time option to print the credits to the console.

**Cleanup/Optimisation**

- Condensed comment search function thanks to new subredditList config key.
- Removed unnecessary failedStats check in fetch().
- Changed initialiseGlobals() to no longer unnecessarily pass empty lists..
- Removed unused import.
- Removed python3 env in main.py.
- Readibility improvements in settings.py.

**Dependencies**

- alive_progress; added.

**Documentation/Logs**

- Added a progress bar to console output (not saved to log file).
- Added a "How to use this menu" option to the settings menu.
- Clarified log messages for when OSCR counts less comments than the set limit.
- Added a log message to ``--format-cdr`` to indicate when praw.ini is already formatted to OSCR.
- When encountering a JSONDecodeError in getConfig(), OSCR now logs what the error was.
- Added copyright notices to the beginnings of all files except setup.py and \__init__.py
- Added a note giving a minimum recommended cutoff of 15 minutes.
- Corrected a spelling error in README.md.
- Moved credits from main.py to CREDITS.md.

**Bug Fixes**

- Fixed int and boolean based keys not being updated by the settings menu.

1.1.1
-----

**Cleanup/Optimisation**

- Removed lingering debug print() statement.

**Documentation/Logs**

- Added copyright notices; one at the beginning of the code in the oscr script file, and one to be printed to the console when OSCR is run.
- Added repository badges/information to README.md

**Bug Fixes**

- Fixed #34: Crash caused by comparing None to int() after settings module output None-type to "limit" in config.json.
- Fixed #35: Converts all numerical limits to None-type.
- Fixed #36: Misleading logs could suggest a bug if available comments are less than the user's limit.

1.1.0
-----

**Meta**

- Renamed project from ClaimDoneRemover (CDR) to Open Source Caretaker for Reddit (OSCR), new PyPi project at: https://pypi.org/project/oscr/

**Functionality**

- Added a settings menu from which you can edit config.json and praw.ini
- Added several run-time arguments;
    - ``--format-cdr`` renames .cdremover and [cdrcredentials] to .oscr and [oscr], respectively,
    - ``--help`` displays a list of commands,
    - ``--no-recur`` forces the program to run only one cycle regardless of 'recur' configuration,
    - ``--reset-config`` resets the config file to defaults,
    - ``--settings`` runs the settings menu.
- OSCR will now stop attempting to update each statistic after a failure to do so.
- OSCR now defaults non-numeric instances of config["limit"] to None type
- Global variables are now contained in gvars class, passed into all necessary functions.
- config is now a global variable.

**Cleanup/Optimisation**

- Switched from .format() to fstrings for more succinct string formatting.
- Squashed some code verbosity; unnecessary variable declarations, if statements with longer conditions than neeeded, etc.
- Removed unnecessary imports.
- fetch() and update() no longer unnecessarily globalise variables.

**Documentation/Logs**

- Replaced the Notes section in README.md with a more informative Additional Help and FAQ section.
- Corrected minor spelling errors in log output and commenting.
- Avoided potential double timestamp in log noting failure to decode config.json.
- createIni() now logs its attempts to create praw.ini

**Bug Fixes**

- #26: New "deleted" lines are appended to stats.txt rather than just updating one line as was intended.
- #27: Potential error with displaying log message in the format "X/None comments checked successfully".
- #28: Potential error with displaying log message in the format "X/Y comments checked successfully" where X is greater than Y.
- #29: Incorrect INI Path for Windows (thanks to /u/--B_L_A_N_K--)
- #31: Program crash on attempting to fetch config.json if the parent directory is missing (see note 6).
- #32: Potential crash if config['logUpdates'] configuration was set to false.

1.0.0
-----

**Meta**

- Created PyPi package for the project, link at: https://pypi.org/project/cdremover/1.0.0/

**Functionality**

- Program is now run through cdremover script (can be used a console command if installed through pip).
- Program now creates praw.ini if it cannot be found (fix for #23).
- Added new cutoffUnit config variable, which is the unit of time the cutoff is measured in converted to seconds.
- Program now resets any search limit value greater than or equal to 1000 to "None", rather than allowing values greater than 1000 to go unchanged, which could have potentially caused issues with Reddit's API.
- Made home, log and version variables global throughout all files and functions.

**Cleanup/Optimisation**

- Renamed libcdr module cdrmodules; included main.py.
- Optimisation improvements for both increased speed and reduced file size.

**Dependencies**

- Moved dependencies from requirements.txt to setup.py so pip will auto-install them.
- Added configparser to dependencies.

**Documentation/Logs**

- Moved log and statistics to ~/.cdremover/data.
- Moved config.json to ~/.cdremover.
- Program now logs the following;
    - every time it intentionally exits,
    - output related to praw.ini handling,
    - a check for each 25 comments successfully checked.
- Clarified ambiguity in some log messages.
- misc.py functions now log console output.
- Re-wrote README.md to faciliate new installation instructions and other information.
- Began recording release candidate versions during development.
- Added/clarified some commenting.

**Bug Fixes**

- #23: Crash if praw.ini is missing or exists without "cdrcredentials" section.
- #24: Crash due to getTime() being declared after the import of a function that attempts to import it.

0.4.5
-----

**Cleanup/Optimisation**

- Moved updateLog() from main.py to log.py.
- Moved getDate() from main.py to misc.py.

**Documentation/Logs**

- Program now gives meaningful log on failure to decode config.json.
- Program now logs what version it is being run with.

0.4.4
-----

**Functionality**

- Program now creates a config file using default settings if one is not present. (fixes #18)
- Now passes logUpdates variable through every attempt to update the log. (fixes #20)
- Changed default cutoff to 1 hour.

**Documentation/Logs**

- Changed to .json config file.

**Bug Fixes**

- #18: New version downloads may overwrite config files.
- #20: Failing to update the log results in a crash.

0.4.3
-----

**Functionality**

- Added "torOnly" configuration, to give the user the option to limit the bot to only detect comments from r/transcribersofreddit. Set to True by default.
- Added "claiming" to the default blacklist.
- Program is no longer case sensitive (i.e. dones and claims containing uppercase letters will still be deleted).

**Documentation/Logs**

- Program now logs upon finding a blacklisted comment that is not past the cutoff (i.e. "Waiting for 'x comment'.").

0.4.2
-----

**Functionality**

- Added automated "unclaim" to the default blacklist.

0.4.1
-----

**Bug Fixes**

- #17: TypeError on attempting to delete comment.

0.4.0
-----

**Cleanup/Optimisation**

- Restructured libcdr library.
- Improved coding and variable names in a few areas.
- Improved error management (part of #14 fix).

**Documentation/Logs**

- Restructured console output and log.
- Added timestamps to console output and log
- Added basic commenting.

**Bug Fixes**

- #14: Updates log twice per iteration, almost doubling log.txt file.

0.3.1
-----

**Functionality**

- Program now auto-creates log.txt if it is absent (part of #11 fix).

**Bug Fixes**

- #11: Program crashes if data folder is absent.
- Corrected a mistake in the blacklist causing automated done not to be deleted.

0.3.0
-----

**Functionatity**

- Added ability to configure whether the program keeps refreshing or only runs through once; recur set to True by default.
- Added automated done/claim to the default blacklist.

**Cleanup/Optimisation**

- Improved readability in some places, especially config.py.

**Documentation/Logs**

- Data folder is now absent in initial download (part of #9 fix).
- Added note that putting your OS in config.py is optional, and only there for the user_agent header.
- Added a long-needed credit.

**Bug Fixes**

- Fixed #8: Program crashes if no stats.txt file is found.
- Fixed #9: Updates could overwrite old statistics and logs with empty files.



0.2.1
-----

**Documentation/Logs**

- Changed output formatting to inline for "Updating log..."
- Added notice that the bot is non-official

0.2.0
-----

**Functionality**

- Added configuration options for limit, wait, and unit; set to 100, 10 and minutes by default.
- Added configuration options for the log; set to True by default.
- Added "unclaim" to the default blacklist.

**Cleanup/Optimisation**

- Removed unused "import datetime" from main.py.

**Documentation/Logs**

- Added a counter to show more detailed real-time output.
- Added a system that logs the console to a .txt file if turned on
- Added a system to save the total statistics for the counter.

**Bug Fixes**

- Fixed #1: Does not continually delete comments as they reach cutoff.

0.1.0
-----

**Functionality**

- Initial program created.
