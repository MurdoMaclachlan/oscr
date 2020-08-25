user = "" # Your username.
os = "" # Your operating system.
blacklist = ["claim", "done"] # The exact, word-for-word body of the comments to be deleted.
cutoff = 3 # The number of hours old which comments must be before they are deleted.
limit = 100 # How many comments to check through in the user's history, max 1000 (enter None).
wait = 10 # How many units of time the program should wait before checking for new comments.
unit = ["minute", "minutes", 60] # The unit of time used for the wait configuration. The number should be the unit converted into seconds.
updateLog = True # Whether or not the log.txt file should be updated. Change to "False" if you don't want new logs.
