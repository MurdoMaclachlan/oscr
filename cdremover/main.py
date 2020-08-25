#!/usr/bin/env python3
import praw
import time
from config import blacklist, cutoff, os, user

version = "0.1"

def getDate(comment):
	return comment.created_utc

while True:
    reddit = praw.Reddit("credentials", user_agent=os+":claimdoneremover:v"+version+" (by u/MurdoMaclachlan)")

    for comment in reddit.redditor(user).stream.comments():
        if comment.body in blacklist:
            if time.time()-getDate(comment)>cutoff*3600:
                print("Past its sell-by date; deleting.")
                comment.delete()
    print("Connection lost. Reconnecting...")
