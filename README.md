# OSCR (Open Source Caretaker for Reddit)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/MurdoMaclachlan/oscr/graphs/commit-activity)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/MurdoMaclachlan/oscr)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/murdo@maclachlans.org.uk)  
[![Documentation Status](https://readthedocs.org/projects/oscr/badge/?version=latest)](https://oscr.murdomaclachlan.dev/en/stable/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/MurdoMaclachlan/oscr)](https://github.com/MurdoMaclachlan/oscr/issues)
![GitHub pull requests](https://img.shields.io/github/issues-pr/MurdoMaclachlan/oscr)
[![GitHub license](https://img.shields.io/github/license/MurdoMaclachlan/oscr)](https://github.com/MurdoMaclachlan/oscr/blob/master/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/MurdoMaclachlan/oscr)](https://github.com/MurdoMaclachlan/oscr/releases/latest)
![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/MurdoMaclachlan/oscr/latest)
![GitHub repo size](https://img.shields.io/github/repo-size/MurdoMaclachlan/oscr)

**This is an unofficial program and is not officially endorsed by the Transcribers of Reddit; they are in no way involved with this program and are not liable for any matters relating to it. This is developed unofficially, in my capacity as a *volunteer*, NOT a moderator.**

**WARNING: use of this bot can cause the ToR-Stats Discord bot to freeze, if you have the bad luck to delete a comment while it is being processed. This has happened to at least two users (including myself).**

More lovingly known as Oscar, this program removes blacklisted comments after a period of time. It is designed with r/TranscribersOfReddit transcribers in mind; specifically those who are tired of these comments clogging up their profiles, thus the contents of the default blacklist.

If set to recur, this program should delete new blacklisted comments periodically as they move past the cutoff time.

## Installation and Use

1. Run either `python3 -m pip install oscr` or `pip3 install oscr` in your command line. It should automatically install the program as well as any dependencies.
2. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to `https://www.reddit.com/prefs/apps/` and creating a new app:
- Give it a name ("Oscar" or "OSCR" are easy to remember).
- Choose "script". 
- Give it a description (which can really be anything you want).
- Set an about url and redirect uri. The about url doesn't matter (I just linked to the project's repository), and the redirect uri only matters if you're using refresh tokens.
3. Now, in your console, run the command `oscr` and you will be prompted to enter information for both config.json and praw.ini. The praw.ini will ask for your client id and client secret, which you can see on `https://www.reddit.com/prefs/apps/`. Go to the page and scroll down until you find the bot you created. Underneath its name should be "personal use script", and below that a string of random characters. This is your client id. If you can't see a field that labeled "secret" with another, longer string of random characters after it, then click the edit button and it should appear (along with other fields you filled out when you were creating the bot). Once praw.ini is created, the program will exit and you will need to rerun it (this is because PRAW currently can't reload praw.ini files once Reddit() has been initialised).

Once it has been created, the contents of your praw.ini file should look something like this:
```
[oscr]
client_id=lI3fAkE7x82LiE
client_secret=4lS0f4Ke1234567894NdN0tR3aL
username=testuser
password=yourpasswordhere
```
You can check if they are correct by navigating to your config folder, which should be .config on Linux and Mac, and AppData on Windows.

4. Once you've rerun the program, each comment older than the cutoff should be deleted. By default, it will search every 10 minutes, and you can then either leave the program running in the background to delete posts in real time as they reach the cutoff, or you could turn recur off in your config file and manually run it every now and then.

To update the program to a newer version, run `python3 -m pip install --upgrade oscr` or `pip3 install --upgrade oscr` in your command line.

## Editing the Config File

Once properly intialised, there should be a `config.json` file in the following directory: `[your home folder]/.oscr`. Its contents will look like this:
```
{
    "config": [
        {
            "blacklist": [
                "claim",
                "done",
                "unclaim",
                "claim -- this was a automated action. please contact me with any questions.",
                "done -- this was a automated action. please contact me with any questions.",
                "unclaim -- this was a automated action. please contact me with any questions.",
                "claiming"
            ],
            "cutoff": 1,
            "cutoffUnit": 3600,
            "limit": 100,
            "logUpdates": true,
            "os": "[Your OS here]",
            "recur": true,
            "regexBlacklist": [
                "^claim(?!(.|\n)*treasure[\s-]*hunt)",
                "^done(?!(.|\n)*treasure[\s-]*hunt)",
                "^unclaim(?!(.|\n)*treasure[\s-]*hunt)"
            ],
            "unit": [
                "minute",
                "minutes",
                60
            ],
            "user": "[Your username here]",
            "useRegex": False,
            "subredditList": [
                "transcribersofreddit"
            ],
            "wait": 10
        }
    ]
}
```

Name | Type | Description
--------|----|-----------
blacklist | Array | The list of comments OSCR will delete. It is not case sensitive, so comments of varying capitalisation will all be deleted, however they will only be deleted if the entire content of the comment matches one of the entries in the blacklist.
cutoff | Integer | The number of units of time old a comment must be before it will be deleted. This is set to 1 by default. I would recommend a minimum cutoff of 15 minutes, in case the u/transcribersofreddit bot has lag and doesn't register your comment in time.
cutoffUnit | Integer | The unit of time used for the cutoff, converted into seconds. This is set to 3600 (1 hour) by default.
limit | Integer | The number of comments the program will check through on your profile; i.e. how far back it will go. This is set to 100 by default and can go to a maximum of 1000 (converted to None by the program), due to Reddit's API limits.
logUpdates | Boolean | Determines whether or not OSCR will write the log to a  file. Set to true by default.
os | String | Your operating system. Can be left blank.
printLogs | Boolean | Determines whether or not OSCR will print log output to the console. Set to true by default.
recur | Boolean | Determines whether the program will run through only once (if False), or continue re-checking your profile in regular intervals until you exit (if True). It is set to True by default. The length of time between program iterations is determined by the **wait** variable.
regexBlacklist | Array | An alternative blacklist intended for use with regexes. Users not familiar with regexes are advised to ignore this list, as regexes are turned off by default and can cause harm to your profile if used without care.
subredditList | Array | The list of subreddits that OSCR cares about. Comments that are int he blacklist or match your set regexes, but are on subreddits *not* in this list, will not be deleted.
unit | Array | A list containing all the variations on the unit of time used for the **wait** variable; singular word, plural word, and integer equivalent converted into seconds. The default unit is minutes.
user | String | Your Reddit username.
useRegex | Boolean | Determines whether the program should use the blacklist key, only deleting comments that exactly match it, or the regexBlacklist key, which allows for more flexible and powerful control over what the programs delete. It is set to False by default, and users not familiar with regexes should leave it this way, as getting your regex wrong can result in OSCR deleting a lot more than you intend.
wait | Integer | The number of units of time (unit being determined by the **unit** variable) OSCr will wait before re-checking your comments. It is set to 10 by default.

You can edit the config.json and praw.ini files from within OSCR by running `oscr --settings`.

## Using the latest testing version

To use the latest testing version, download the 2.x branch files (0.x is deprecated), extract the archive you have downloaded, and use `pip3 install .` after navigating into the directory the files were extracted to.

## Additional Help and FAQ

**Where are the config file and data located?**\
On all operating systems, these are stored under `/home/your_username/.oscr/`, with the data (log and statistics) under the subfolder `data`.

**Where is the praw.ini file?**\
On Linux, this is under `/home/your_username/.config/oscr`,
on MacOS it should be under `/home/your_username/.config/oscr`,
and on Windows, it is under `C:\Users\your_username\AppData\Roaming\oscr`.

**What if I already have a praw.ini on my computer?**\
Saving in an `oscr` subfolder prevents OSCR from overwriting this ini, and the program is designed to only pull from that file. If you are updating from a version of OSCR that had the praw.ini in just `.config`, run `oscr -F` and it should automatically move the `oscr` section from your `.config` praw.ini to `.config/oscr`.

**How can I contact the developer?**\
I'm reachable through `murdo@maclachlans.org.uk` and `murdomaclachlan@gmail.com` (the first address is preferred). You can also open an issue on GitHub if needed.
