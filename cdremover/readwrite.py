def fetch(statistic):

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
    return int(''.join(result))

def update(statistic, value):

    lineToReplace = 0
    newLine = "{}: {}".format(statistic, str(value))

    with open("data/stats.txt", "r") as file:
        content = file.read().splitlines()

    with open("data/stats.txt", "w") as file:
        if content == []:
            file.write(newLine)
            return "Updated successfully."

        for line in content:
            if list(line)[0] == list(statistic)[0]:
                lineToReplace = content.index(line)

        content[lineToReplace] = newLine

        file.write('\n'.join(content))

    return "Updated successfully."
