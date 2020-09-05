user = "" # Your username.
os = "" # Your operating system (optional; for the user_agent header).
blacklist = [
    "claim",
    "done",
    "unclaim",
    "claim -- this was a automated action. please contact me with any questions.",
    "done -- this was a automated action. please contact me with any questions.",
    "unclaim -- this was a automated action. please contact me with any questions.",
    "claiming"
] # The exact, word-for-word body of the comments to be deleted.
cutoff = 3 # The number of hours old which comments must be before they are deleted.
limit = 100 # How many comments to check through in the user's history, max 1000 (enter None).
wait = 10 # How many units of time the program should wait before checking for new comments.
unit = [
    "minute",
    "minutes",
    60
] # The unit of time used for the wait configuration. The number should be the unit converted into seconds.
logUpdates = True # Whether or not the log.txt file should be updated. Change to "False" if you don't want new logs.
recur = True # Whether or not you want the program to keep re-checking; disable if you want to just run once manually.
torOnly = True # Whether or not you want the program to only delete comments posted in r/transcribersofreddit.
