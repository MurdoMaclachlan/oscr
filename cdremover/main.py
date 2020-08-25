#!/usr/bin/env python3
import praw
import time
import libcdr
from config import blacklist, cutoff, limit, os, unit, user, wait

version = "0.2 dev"

def getDate(comment):
	return comment.created_utc

# Credit to u/--B_L_A_N_K-- for improving the system and allowing it to delete in real-time, as well as for writing the improved console output and its formatting.

reddit = praw.Reddit("credentials", user_agent=os+":claimdoneremover:v"+version+" (by u/MurdoMaclachlan)")

totalCounted = libcdr.fetch("counted")
totalDeleted = libcdr.fetch("deleted")

while True:
	deleted = 0
	counted = 0
	nonCutoff = 0
	for comment in reddit.redditor(user).comments.new(limit=limit):
		if comment.body in blacklist:
			if time.time() - getDate(comment) > cutoff*3600:
				comment.delete()
				deleted += 1
			else:
				nonCutoff += 1
		counted += 1

	totalCounted += counted
	totalDeleted += deleted
	libcdr.update("counted", totalCounted)
	libcdr.update("deleted", totalDeleted)
	print("Totals:\nCounted: {}\nDeleted: {}\n".format(str(totalCounted),str(totalDeleted)))
	print("This Run:\nCounted: {}\nDeleted: {}\nWaiting For: {}\n".format(str(counted),str(deleted),str(nonCutoff)))
	if wait == 1:
		print("Waiting 1 {} before checking again...\n\n---").format(unit[0])
	else:
		print("Waiting {} {} before checking again...\n\n---".format(str(wait), unit[1]))
	time.sleep(wait*unit[2])
