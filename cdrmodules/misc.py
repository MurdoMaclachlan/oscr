import datetime
import time
import json
import sys

# Retrieves the user configurations from a .json file, or creates a config file from default values if one can't be found.
def getConfig(home):
    try:
        with open(home+"/.cdremover/config.json") as configFile:
            try:
                fromConfig = json.load(configFile)
            except json.decoder.JSONDecodeError:
                currentTime = getTime(time.time())
                print("{} - Failed to get config; could not decode JSON file. Exiting.".format(currentTime))
                sys.exit(0)
            config = fromConfig["config"][0]
   
    except FileNotFoundError:
        user = input("No config file found. Please enter your Reddit username:  /u/")
        os = input("Optionally, you may also enter your operating system. This is only used in the user_agent and can be left blank by simply pressing enter:  ")
        defaultConfig = {
            "user": user,
            "os": os,
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
            "wait": 10,
            "unit": [
                "minute",
                "minutes",
                60
            ],
            "logUpdates": True,
            "recur": True,
            "torOnly": True
        }
        outConfig = {}
        outConfig["config"] = []
        outConfig["config"].append(defaultConfig)
        
        with open(home+"/.cdremover/config.json", "w") as outFile:
            outFile.write(json.dumps(outConfig, indent=4, sort_keys=True))
            
        config = outConfig["config"][0]

    if config["limit"] == 1000:
        config["limit"] = None

    return config

# Creates praw.ini file, if it is missing
def createIni(home):
    platformConfs = {
        "linux": ".config",
        "darwin": ".config",
        "win32": "AppData"
    }
    print("No praw.ini file found. It will need to be created.")
    iniVars = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": input("Please input your Reddit username:  /u/"),
        "password": input("Please input your Reddit password:  ")
    }
    with open(home+"/"+platformConfs[sys.platform]+"/praw.ini", "a+") as file:
        file.write("[credentials]")
        for i in iniVars:
            file.write(iniVars[i])
              
# Finds the current time and returns it in a human readable format.
def getTime(timeToFind):
    currentTime = datetime.datetime.fromtimestamp(timeToFind)
    return currentTime.strftime("%Y-%m-%d %H:%M:%S")

# Retieves the date the comment was posted at.
def getDate(comment):
    return comment.created_utc
