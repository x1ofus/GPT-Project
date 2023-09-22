# This script takes the discordlog.json file and parses it into a usuable data set

import json
import re

# input file
file = open("GPT/data/masterdiscordlogs.json", encoding='utf-8')
dataLog = json.load(file)

# output file
outFileUserless = open("GPT/data/dataset-userless.txt", 'w', encoding='utf-8')
outFileUser = open("GPT/data/dataset.txt", 'w', encoding='utf-8')

# username is stored as an index of an array so get an array and convert the userID to the username
userList = [dataLog["meta"]["users"][userID]["name"] for userID in dataLog["meta"]["userindex"]]

channelID = list(dataLog["meta"]["channels"].keys())[0]

# store the message entries in a list
messageEntries = []

for user, data in dataLog["data"][str(channelID)].items():
    # add nametag to message
    # message = userList[data["u"]] + ':\n'
    message = ""
    
    # m is for data containing messages
    if "m" in data:
        # re.sub("<:\W:\d+>", "", data["m"])    # remove custom emojis
        messageContents = data["m"]
        # regular expression to replace mentions in "<@discordID>" to @username format
        messageContents = re.sub("<@!\d+>", lambda uid : "@" + dataLog["meta"]["users"][uid.group()[3 : -1]]["name"], messageContents)
        messageContents = re.sub("<@\d+>", lambda uid : "@" + dataLog["meta"]["users"][uid.group()[2 : -1]]["name"], messageContents)
        messageContents = re.sub("https?:\/\/\S*([\s+]|$)", "", messageContents) 
        messageContents = re.sub("\<a?:.+\>", "", messageContents) 
        if not messageContents or message: 
            continue
        message += messageContents
    else:
        continue
        
    # a is for data containing explicitly links/urls
    # elif "a" in data:
        # message += data["a"][0]["url"]
    
    # add message to message list with timestamp
    message += "\n"
    messageEntries.append((data["t"], message, userList[data["u"]] + ":\t" + message))

# sort messages based on timestamp
messageEntries.sort()

# add messages to file
for message in messageEntries:
    # outFile.write(repr(message[1]))
    outFileUserless.write(message[1])
    outFileUser.write(message[2])

file.close()
outFileUser.close()
outFileUserless.close()

print("Done")