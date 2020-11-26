# OSCR (Open Source Caretaker for Reddit)

**This is an unofficial program and is not officially endorsed by the Transcribers of Reddit; they are in no way involved with this program and are not liable for any matters relating to it.**

**WARNING: use of this bot can cause the ToR-Stats Discord bot to freeze, if you have the bad luck to delete a comment while it is being processed. This has happened to at least two users (including myself).**

More lovingly known as Oscar, this program removes blacklisted comments after a period of time. It is designed with r/TranscribersOfReddit transcribers in mind; specifically those who are tired of these comments clogging up their profiles, thus the contents of the default blacklist.

If set to recur, this program should delete new blacklisted comments periodically as they move past the cutoff time.

## Installation and Use

1. Run either `python3 -m pip install cdremover` or `pip3 install cdremover` in your command line. It should automatically install the program as well as any dependencies.
2. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to `https://www.reddit.com/prefs/apps/` and creating a new app. 
    Give it a name ("Oscar" or "OSCR" are easy to remember).
    Choose "script". 
    Give it a description (which can really be anything you want).
    Set an about url and redirect url. They don't really matter for a personal script. I linked to this repository.
3. Now, in your console, run the command `cdremover` and you will be prompted to enter information for both config.json and praw.ini. The praw.ini will ask for your client id and client secret, which you can see on `https://www.reddit.com/prefs/apps/`. Go to the page and scroll down until you find the bot you created. Underneath its name should be "personal use script", and below that a string of random characters. This is your client id. If you can't see a field that labeled "secret" with another, longer string of random characters after it, then click the edit button and it should appear (along with other fields you filled out when you were creating the bot). Once praw.ini is created, the program will exit and you will need to rerun it (this is because PRAW currently can't reload praw.ini files once Reddit() has been initialised).

Once it has been created, the contents of your praw.ini file should look something like this:
```
[cdrcredentials]
client_id=lI3fAkE7x82LiE
client_secret=4lS0f4Ke1234567894NdN0tR3aL
username=testuser
password=yourpasswordhere
```
You can check if they are correct by navigating to your config folder, which should be .config on Linux and Mac, and AppData on Windows.

4. Once you've rerun the program, each comment older than the cutoff should be deleted. By default, it will search every 10 minutes, and you can then either leave the program running in the background to delete posts in real time as they reach the cutoff, or you could turn recur off in your config file and manually run it every now and then.

To update the program to a newer version, run `python3 -m pip install --upgrade oscr` or `pip3 install --upgrade oscr` in your command line.

## Editing the Config File

Once properly intialised, there should be a `config.json` file in the following directory: `[your home folder]/.oscar`. Its contents will look like this:
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
            "torOnly": true,
            "unit": [
                "minute",
                "minutes",
                60
            ],
            "user": "[Your username here]",
            "wait": 10
        }
    ]
}
```
- The blacklist is the list of comments it will delete if it comes across. It is not case sensitive, so comments of varying capitalisation will all be deleted, however they will only be deleted if the entire content of the comment matches one of the entries in the blacklist.
- The cutoff is the number of units of time old a comment must be before it is deleted. This is set to 1 by default.
- The cutoffTime is one of the unit of time used for the cutoff, converted into seconds. This is set to 3600 (1 hour) by default.
- The limit is the number of comments the program will check through on your profile; i.e. how far back it will go. This is set to 100 by default, and can go to a maximum of 1000. This maximum is due to Reddit's own API limits.
- logUpdates is a boolean (true/false) variable that determines whether the program will write the console log to a file. This is set to true by default.
- The os is your operating system, and can be left blank.
- recur is a boolean variable that determines whether the program will run only once (false), or continue searching through until you exit it (true). This is set to true by default.
- torOnly is whether the program will delete blacklisted comments on all subreddits (false), or only on r/transcribersofreddit (true). This is set to true by default.
- The unit list contains variations on the unit of time used for the wait variable; singular, plural, and the equivalent of one of the unit when converted into seconds. The unit is minutes by default.
- user is your Reddit username.
- wait is how many units of time the program waits before re-checking your comments. This is set to 10 by default.

You will have a `data` folder in `.cdremover`, which is where the `log.txt` and `stats.txt` files are saved.

## Using the latest testing version

To use the latest testing version, download either the 1.x branch files (0.x is deprecated), extract the archive you have downloaded, and use `pip3 install .` after navigating into the directory the files were extracted to.

## Notes

- If you already have a praw.ini file in your config folder, this program should append the cdrcredentials section to it without altering any content that is already there. If you notice any errors with this, please report them immediately.
