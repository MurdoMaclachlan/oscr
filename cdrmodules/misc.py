import datetime
import time
import json
import sys
from .gvars import *
from os import environ, mkdir
from os.path import isfile, isdir

# Finds the current time and returns it in a human readable format.
def getTime(timeToFind):
    currentTime = datetime.datetime.fromtimestamp(timeToFind)
    return currentTime.strftime("%Y-%m-%d %H:%M:%S")

from .log import doLog, writeLog

# Retrieves the user configurations from a .json file, or creates a config file from default values if one can't be found.
def getConfig():
    
    global home, log

    try:
        with open(home+"/.cdremover/config.json") as configFile:
            try:
                fromConfig = json.load(configFile)
            except json.decoder.JSONDecodeError:
                doLog("Failed to get config; could not decode JSON file. Exiting.")
                sys.exit(0)
            config = fromConfig["config"][0]
   
    except FileNotFoundError:
        user = input("No config file found. Please enter your Reddit username:  /u/")
        os = input("Optionally, you may also enter your operating system. This is only used in the user_agent and can be left blank by simply pressing enter:  ")
        defaultConfig = {
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
            "logUpdates": True,
            "os": os,
            "recur": True,
            "unit": [
                "minute",
                "minutes",
                60
            ],
            "user": user,
            "torOnly": True,
            "wait": 10
        }
        outConfig = {}
        outConfig["config"] = []
        outConfig["config"].append(defaultConfig)
        
        try:
            dumpConfig(outConfig)
        except FileNotFoundError:
            doLog("home/.cdremover directory not found; creating.")
            if not isdir(home+"/.cdremover"):
                mkdir(home+"/.cdremover")
                dumpConfig(outConfig)
            
        config = outConfig["config"][0]
        
    # Performs any necessary one-time calculations and changes relating to the config
    if config["limit"] >= 1000 or not str(config["limit"]).isnumeric():
        config["limit"] = None
    try:
        config["cutoffSec"] = config["cutoff"]*config["cutoffUnit"]
    except (KeyError, TypeError):
        config["cutoffSec"] = config["cutoff"]*3600
    config["waitTime"] = config["wait"]*config["unit"][2]

    return config

# Attempts to update the config file
def dumpConfig(outConfig):
    with open(home+"/.cdremover/config.json", "w") as outFile:
        outFile.write(json.dumps(outConfig, indent=4, sort_keys=True))
    return True

# Creates praw.ini file, if it is missing
def createIni():
    
    global home

    platformConfs = {
        "linux": ".config",
        "darwin": ".config"
    }
    if sys.platform.startswith("win"):
        savePath = environ["APPDATA"]
    else:
        savePath = home + platformConfs[sys.platform]
    print("praw.ini incomplete or incorrect. It will need to be created.")
    iniVars = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": input("Please input your Reddit username:  /u/"),
        "password": input("Please input your Reddit password:  ")
    }
    with open(savePath+"/praw.ini", "a+") as file:
        file.write("[cdrcredentials]\n")
        for i in iniVars:
            file.write(i+"="+iniVars[i]+"\n")
    return True
             
# Retrieves the date the comment was posted at.
def getDate(comment):
    return comment.created_utc
