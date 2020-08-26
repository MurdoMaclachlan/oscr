#!/usr/bin/env python3
import praw
import time
import libcdr
from config import *

version = "0.2.1"

def getDate(comment):
	return comment.created_utc

# Credit to u/--B_L_A_N_K-- for improving the system and allowing it to delete in real-time, as well as for writing the improved console output and its formatting.

reddit = praw.Reddit("credentials", user_agent=os+":claimdoneremover:v"+version+" (by u/MurdoMaclachlan)")

log = []

totalCounted = libcdr.fetch("counted", log)
totalDeleted = libcdr.fetch("deleted", log)

if updateLog == True:
	libcdr.doLog("Updating log...", log)
	libcdr.writeLog(log)

while True:
	log = []
	deleted = 0
	counted = 0
	nonCutoff = 0

	for comment in reddit.redditor(user).comments.new(limit=limit):
		if comment.body in blacklist:
			if time.time() - getDate(comment) > cutoff*3600:
				libcdr.doLog("Obsolete '{}' found, deleting.".format(comment.body), log)
				comment.delete()
				deleted += 1
			else:
				nonCutoff += 1
		counted += 1

	totalCounted += counted
	totalDeleted += deleted
	libcdr.update("counted", totalCounted, log)
	libcdr.update("deleted", totalDeleted, log)
	libcdr.doLog("Totals:\nCounted: {}\nDeleted: {}\n".format(str(totalCounted),str(totalDeleted)), log)
	libcdr.doLog("This Run:\nCounted: {}\nDeleted: {}\nWaiting For: {}\n".format(str(counted),str(deleted),str(nonCutoff)), log)
	if wait == 1:
		libcdr.doLog(("Waiting 1 {} before checking again...\n\n---").format(unit[0]), log)
	else:
		libcdr.doLog("Waiting {} {} before checking again...\n\n---".format(str(wait), unit[1]), log)

	if updateLog == True:
		libcdr.doLog("Updating log...\n---", log)
		libcdr.writeLog(log)

	time.sleep(wait*unit[2])
