from .log import doLog

def fetch(statistic, log, home):
    
    result = []

    # If stats.txt doesn't exist, this returns 0. Otherwise it reads the file.
    try:    
        with open(home+"/.cdremover/data/stats.txt", "r") as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        doLog("No stats for {} found; returning 0.".format(statistic), log)
        return 0

    # If it can't find a value for any statistic, this returns 0.
    if content == []:
        doLog("No stats for {} found; returning 0.".format(statistic), log)
        return 0
    
    # If it can find the value for the statistic being fetched, this returns it. (I swear this shithole of a for-if-for-if tree must be condensable)
    for line in content:
        if list(line)[0] == list(statistic)[0]:
            found = True
            for i in list(line):
                if i.isnumeric():
                    result.append(str(i))
            break
        else:
            found = False

    # If it can only find one statistic, and it isn't the one being fetched, this returns 0.
    if found == False:
        doLog("No stats for {} found; returning 0.".format(statistic), log)
        return 0

    doLog("Fetched {} successfully.".format(statistic), log)
    return int(''.join(result))

def update(statistic, value, log, home):

    content = []    
    lineToReplace = 0
    newLine = "{}: {}".format(statistic, str(value))

    # Creates the stats.txt file if it doesn't exist.
    try:
        with open(home+"/.cdremover/data/stats.txt", "r") as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        doLog("No stats.txt found; creating.", log)

    with open(home+"/.cdremover/data/stats.txt", "w") as file:
        
        # If it can't find any statistics, this adds the statistic to be updated and sets the other to 0.
        if content == []:
            if statistic == "counted":
                file.write(newLine+"\ndeleted: 0")
            else:
                file.write("counted: 0\n"+newLine)
            doLog("Updated {} successfully.".format(statistic), log)
            return True

        # If it can find both statistics, this updates as normal.
        for line in content:
            if list(line)[0] == list(statistic)[0]:
                found = True
                lineToReplace = content.index(line)
                break
            else:
                found = False
        
        # If it can only find one statistic, and it isn't the right one, this adds the right one.
        if found == False:
            content.append(newLine)
            file.seek(0)
            file.write('\n'.join(content))
            doLog("Updated {} successfully.".format(statistic), log)
            return True
                
        content[lineToReplace] = newLine

        file.write('\n'.join(content))

    doLog("Updated {} successfully.".format(statistic), log)
    return True