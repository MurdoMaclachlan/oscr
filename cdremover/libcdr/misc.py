import datetime
import json

# Retrieves the user configurations from a .json file, or creates a config file from default values if one can't be found.
def getConfig():
    try:
        with open("config.json") as configFile:
            fromConfig = json.load(configFile)
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
        
        with open("config.json", "w") as outFile:
            outFile.write(json.dumps(outConfig, indent=4, sort_keys=True))
            
        config = outConfig["config"][0]

    if config["limit"] == 1000:
        config["limit"] = None

    return config

# Finds the current time and returns it in a human readable format.
def getTime(timeToFind):
    currentTime = datetime.datetime.fromtimestamp(timeToFind)
    return currentTime.strftime("%Y-%m-%d %H:%M:%S")
