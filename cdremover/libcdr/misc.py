def doLog(output, log):
    log.append(output+"\n")
    print(output)
    return True

def writeLog(log):
    with open("data/log.txt", "a") as file:
        for i in log:
            file.write(i)
    return True
