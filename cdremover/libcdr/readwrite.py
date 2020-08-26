from .misc import doLog

def fetch(statistic, log):

    try:    
        file = open("data/stats.txt", "r")
    except FileNotFoundError:
        doLog("No stats for {} found; returning 0.".format(statistic), log)
        return 0
    
    content = file.read().splitlines()
    result = []

    # If it can't find any statistics
    if content == []:
        doLog("No stats for {} found; returning 0.".format(statistic), log)
        return 0
    
    # If it can find the right statistic (I swear this shithole of a for-if-for-if tree must be condensable)
    for line in content:
        if list(line)[0] == list(statistic)[0]:
            found = True
            for i in list(line):
                if i.isnumeric():
                    result.append(str(i))
            break
        else:
            found = False

    # If it can only find one statistic, and it isn't the right one
    if found == False:
        doLog("No stats for {} found; returning 0.".format(statistic), log)
        return 0

    file.close()
    doLog("Fetched {} successfully.".format(statistic), log)
    return int(''.join(result))

def update(statistic, value, log):

    content = []    
    lineToReplace = 0
    newLine = "{}: {}".format(statistic, str(value))

    try:
        with open("data/stats.txt", "r") as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        doLog("No stats.txt file found; creating.", log)

    with open("data/stats.txt", "w") as file:
        
        # If it can't find any statistics
        if content == []:
            if statistic == "counted":
                file.write(newLine+"\ndeleted: 0")
            else:
                file.write("counted: 0\n"+newLine)
            doLog("Updated {} successfully.".format(statistic), log)
            return True

        # If it can find the right statistic
        for line in content:
            if list(line)[0] == list(statistic)[0]:
                found = True
                lineToReplace = content.index(line)
                break
            else:
                found = False
        
        # If it can only find one statistic, and it isn't the right one
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
