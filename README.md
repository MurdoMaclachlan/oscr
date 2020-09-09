# Claim/Done Remover

**This is an unofficial program and is not officially endorsed by the Transcribers of Reddit; they are in no way involved with this program and are not liable for any matters relating to it.**

Also known as CDRemover, this program removes "claim" and "done" comments after a period of time. It is designed with r/TranscribersOfReddit transcribers in mind; specifically those  who are tired of these comments clogging up their profiles.

If you've been a transcriber for a while, chances are this program will not remove every "claim" or "done" you've ever posted, but when I tested it removed the most recent 60 or so, and if you have it running in the background, it should continually delete them as they pass the cutoff age (NOTE: current master version does not do this. Should be fixed in v0.2).

## Installation and Use

1. Clone the `claimdoneremover` repository to a directory.
2. Run `pip3 install praw` (you might need to do so as root/admin).
3. Inside the `cdremover` folder, if `main.py` is not yet executable, make it so. On Linux you can do this by running `chmod +x main.py` from inside the `cdremover` directory.
4. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to `https://www.reddit.com/prefs/apps/` and creating a new app. 
    Give it a name ("ClaimDoneRemover" or "CDRemover" are easy to remember).
    Choose "script". 
    Give it a description (which can really be anything you want).
    Set an about url and redirect url. They don't really matter for a personal script. I linked to this git.
4. Now open the `praw.ini` file. This will contain the credentials for the app you created, and your account. You need your app's client id (14 characters) and client secret (27 characters), and your username and password.

Once complete, your praw.ini should look like this:
```
[default]
client_id=lI3fAkE7x82LiE
client_secret=4lS0f4Ke1234567894NdN0tR3aL
username=testuser
password=yourpasswordhere
```
Your praw.ini should remain in the current directory when running CDRemover, or in one of the config folders as [described on PRAW's documentation](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html).

5. Once you're done, navigate to the folder where `main.py` is and run the file. It might run with an IDE you have installed, or simply run itself, or you can run it from the command line. On Linux, you do this like so: `./main.py`. 
6. The first time you run the program, it will initialise a `config.json` file, prompting you to enter your username and your operating system. The first of these is needed for the program to work, but the operating system is optional and can be left blank.
7. After this each comment older than the cutoff should be deleted. By default, it will search every 10 minutes, and you can then either leave the program running in the background to delete posts in real time as they reach the cutoff, or you could turn recur off in your config file and manually run it every now and then.

## Editing the Config File

Once properly intialised, there should be a `config.json` file in the same directory as `main.py`. Its contents will look like this:
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
- The cutoff is the amount of hours old a comment must be before it is deleted. This is set to 1 hour by default.
- The limit is the number of comments the program will check through on your profile; i.e. how far back it will go. This is set to 100 by default, and can go to a maximum of 1000. This maximum is due to Reddit's own API limits.
- logUpdates is a boolean (true/false) variable that determines whether the program will right the console log to a file. This is set to true by default.
- The os is your operating system, and can be left blank.
- recur is a boolean variable that determines whether the program will run only once (false), or continue searching through until you exit it (true). This is set to true by default.
- torOnly is whether the program will delete blacklisted comments on all subreddits (false), or only on r/transcribersofreddit (true). This is set to true by default.
- The unit list contains variations on the unit of time used for the wait variable; plural, singular, and the converted into seconds. The unit is minutes by default.
- The user is your Reddit username.
- The wait is how many units of time the program waits before re-checking your comments. This is set to 10 by default.

## Notes

- One user has experienced a recursion error upon initialising a Reddit instance. This appears to have been a result of attempting to initialise with an empty Redditor name, and is now a verified PRAW issue. Don't try to initialise with an empty Redditor name.
