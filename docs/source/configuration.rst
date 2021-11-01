Configuration
==============

Once properly intialised, there should be a ``config.json`` file in the following directory: ``[your home folder]/.oscr``. Its contents will look like this::

   {
       "config": [
           {
               "blacklist": [
                   "claim",
                   "claiming",
                   "claim -- this was a automated action. please contact me with any questions.",
                   "dibs",
                   "done",
                   "done -- this was a automated action. please contact me with any questions.",
                   "unclaim",
                   "unclaiming",
                   "unclaim -- this was a automated action. please contact me with any questions."
               ],
               "caseSensitive": False,
               "cutoff": 1,
               "cutoffUnit": 3600,
               "debug": False,
               "limit": 100,
               "logUpdates": True,
               "os": "[Your OS here]",
               "printLogs": True,
               "recur": True,
               "regexBlacklist": [
                   "^(claim|done|dibs|unclaim)(?!(.|\n)*treasure[\s-]*hunt)"
               ],
               "reportTotals": True,
               "subredditList": [
                   "transcribersofreddit"
               ],
               "unit": [
                   "minute",
                   "minutes",
                   60
               ],
               "useRefreshTokens": False,
               "useRegex": False,
               "userList": [
                   "transcribersofreddit"
               ],
               "wait": 10
           }
       ]
   }

The following is an explanation of what each configuration option does:

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - blacklist
     - Array
     - The list of comments OSCR will delete. It is not case sensitive, so comments of varying capitalisation will all be deleted, however they will only be deleted if the entire content of the comment matches one of the entries in the blacklist.
   * - caseSensitive
     - Boolean
     - When using the blacklist, this value determines whether or not the program is case sensitive in its search for comments. Not applicable when using regexes.
   * - cutoff
     - Integer
     - The number of units of time old a comment must be before it will be deleted. This is set to 1 by default. I would recommend a minimum cutoff of 15 minutes, in case the u/transcribersofreddit bot has lag and doesn't register your comment in time.
   * - cutoffUnit
     - Integer
     - The unit of time used for the cutoff, converted into seconds. Set to 3600 (1 hour) by default.
   * - debug
     - Boolean
     - If set to True, OSCR will log obsolete comments, but not actually delete them. Set to False by default.
   * - limit
     - Integer
     - The number of comments the program will check through on your profile; i.e. how far back it will go. This is set to 100 by default and can go to a maximum of 1000 (converted to None by the program), due to Reddit's API limits.
   * - logUpdates
     - Boolean
     - Determines whether or not OSCR will write the log to a file. Set to true by default.
   * - os
     - String
     - Your operating system. Can be left blank.
   * - printLogs
     - Boolean
     - Determines whether or not OSCR will print log output to the console. Set to true by default.
   * - recur
     - Boolean
     - Determines whether the program will run through only once (if False), or continue re-checking your profile in regular intervals until you exit (if True). It is set to True by default. The length of time between program iterations is determined by the wait variable.
   * - regexBlacklist
     - Array
     - An alternative blacklist intended for use with regexes. Users not familiar with regexes are advised to ignore this list, as regexes are turned off by default and can cause harm to your profile if used without care.
   * - reportTotals
     - Boolean
     - Determines whether or not OSCR will print total statistics to the log and console output. Set to True by default.
   * - subredditList
     - Array
     - The list of subreddits that OSCR cares about. Comments that are in the blacklist or match your set regexes but are not on one of these subreddits will be ignored. If the list is empty, OSCR will check comments on all subreddits.
   * - unit
     - Array
     - A list containing all the variations on the unit of time used for the wait variable; singular word, plural word, and integer equivalent converted into seconds. The default unit is minutes.
   * - useRefreshTokens
     - Boolean
     - Determines whether or not OSCR should authenticate using refresh tokens; enable this if you are using two-factor authentication.
   * - useRegex
     - Boolean
     - Determines whether OSCR should use the blacklist key, only deleting comments that exactly match it, or the regexBlacklist key, which allows for more flexible and powerful control over what the programs delete. It is set to False by default, and users not familiar with regexes should leave it this way, as getting your regex wrong can result in OSCR deleting a lot more than you intend.
   * - userList
     - Array
     - The list of users that OSCR cares about. Comments that are in the blacklist or match your set regexes but are not in reply to one of these users will be ignored. If the list is empty, OSCR will check comments regardless of whom they are in reply to.
   * - wait
     - Integer
     - The number of units of time (unit being determined by the unit variable) OSCr will wait before re-checking your comments. It is set to 10 by default.

You can edit the config.json and praw.ini files from within OSCR by running ``oscr --settings`` or ``oscr -S``.
