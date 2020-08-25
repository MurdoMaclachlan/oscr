from .misc import doLog

def fetch(statistic, log):

    file = open("data/stats.txt", "r")
    content = file.read().splitlines()
    result = []

    # I swear this shithole of a for-if-for-if tree must be condensable
    for line in content:
        if list(line)[0] == list(statistic)[0]:
            for i in list(line):
                if i.isnumeric():
                    result.append(str(i))

    file.close()
    doLog("Fetched {} successfully.".format(statistic), log)
    return int(''.join(result))

def update(statistic, value, log):

    lineToReplace = 0
    newLine = "{}: {}".format(statistic, str(value))

    with open("data/stats.txt", "r") as file:
        content = file.read().splitlines()

    with open("data/stats.txt", "w") as file:
        if content == []:
            file.write(newLine)
            doLog("Updated {} successfully.".format(statistic), log)
            return True

        for line in content:
            if list(line)[0] == list(statistic)[0]:
                lineToReplace = content.index(line)

        content[lineToReplace] = newLine

        file.write('\n'.join(content))

    doLog("Updated {} successfully.".format(statistic), log)
    return True
