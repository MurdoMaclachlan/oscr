from .log import doLog

def fetch(statistic, gvars):
    
    if statistic in gvars.failedStats:
        doLog(f"Skipping fetch of following statistic: {statistic}", gvars)
        return False
    
    result = []

    # If stats.txt doesn't exist, this returns 0. Otherwise it reads the file.
    try:    
        with open(gvars.home+"/.oscr/data/stats.txt", "r") as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        doLog(f"No stats for {statistic} found; returning 0.", gvars)
        return 0

    # If it can't find a value for any statistic, this returns 0.
    if content == []:
        doLog(f"No stats for {statistic} found; returning 0.", gvars)
        return 0
    
    for line in content:
        
        # If it can find the value for the statistic being fetched, this returns it. (I swear this shithole of a for-if-for-if tree must be condensable)
        if list(line)[0] == list(statistic)[0]:
            for i in list(line):
                if i.isnumeric():
                    result.append(str(i))
            break

    # If it can only find one statistic, and it isn't the one being fetched, this returns 0.
    if result == []:          
        doLog(f"No stats for {statistic} found; returning 0.", gvars)
        return 0

    doLog(f"Fetched {statistic} successfully.", gvars)
    return int(''.join(result))

def update(statistic, value, gvars):

    if statistic in gvars.failedStats:
        doLog(f"Skipping update of following statistic: {statistic}", gvars)
        return False

    content = []    
    lineToReplace = 0
    newLine = f"{statistic}: {str(value)}"

    # Creates the stats.txt file if it doesn't exist.
    try:
        with open(gvars.home+"/.oscr/data/stats.txt", "r") as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        doLog("No stats.txt found; creating.", gvars)

    with open(gvars.home+"/.oscr/data/stats.txt", "w") as file:
        
        # If it can't find any statistics, this adds the statistic to be updated and sets the other to 0.
        if content == []:
            if statistic == "counted":
                file.write(newLine+"\ndeleted: 0")
            else:
                file.write("counted: 0\n"+newLine)
            doLog(f"Updated {statistic} successfully.", gvars)
            return True

        for line in content:
            
            # If it can find both statistics, this updates as normal.
            if list(line)[0] == list(statistic)[0]:
                lineToReplace = content.index(line)
                content[lineToReplace] = newLine
                file.write('\n'.join(content))
                doLog(f"Updated {statistic} successfully.", gvars)
                return True
            
        # If it can only find one statistic, and it isn't the right one, this adds the right one.
        content.append(newLine)
        file.seek(0)
        file.write('\n'.join(content))
        doLog(f"Updated {statistic} successfully.", gvars)
        return True
    
    doLog(f"Statistics error: failed to update {statistic}, will no longer attempt to update this statistic for this instance.")
    gvars.failedStats.append(statistic)
    return False
