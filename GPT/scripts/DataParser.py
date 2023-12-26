""" This script takes the discordlog.json file and parses it into a usuable data set

Removes discord links and image embeds
Converts user IDs to user names
Tags each message with the name of the user
"""

import sys
import os
import json
import re

def parse_data(infileName, outfileName):
    
    # input file
    file = open("GPT/data/" + infileName, encoding='utf-8')
    dataLog = json.load(file)

    # username is stored as an index of an array so get an array and convert the userID to the username
    userList = [dataLog["meta"]["users"][userID]["name"] for userID in dataLog["meta"]["userindex"]]

    # ID of the message channel in the logs (choose the first channel)
    channelID = list(dataLog["meta"]["channels"].keys())[0]

    # store the message entries in a list
    messageEntries = []

    for user, data in dataLog["data"][str(channelID)].items():
        # add nametag to message
        message = userList[data["u"]] + ':\t'
        
        # m is for data containing messages
        if "m" in data:
            # re.sub("<:\W:\d+>", "", data["m"])    # remove custom emojis
            messageContents = data["m"]
            # regular expression to replace mentions in "<@discordID>" to @username format
            messageContents = re.sub("<@!\d+>", lambda uid : "@" + dataLog["meta"]["users"][uid.group()[3 : -1]]["name"], messageContents)
            messageContents = re.sub("<@\d+>", lambda uid : "@" + dataLog["meta"]["users"][uid.group()[2 : -1]]["name"], messageContents)
            messageContents = re.sub("https?:\/\/\S*([\s+]|$)", "", messageContents) 
            messageContents = re.sub("\<a?:.+\>", "", messageContents) 

            # if there is no message, skip
            if not messageContents: 
                continue

            message += messageContents
        
            # add message to message list with timestamp
            message += "\n"
            messageEntries.append((data["t"], message, userList[data["u"]] + ":\t" + message))

    # sort messages based on timestamp
    messageEntries.sort()

    # output file 
    outFile = open("GPT/data/" + outfileName, 'w', encoding='utf-8')

    # add messages to file
    for message in messageEntries:
        outFile.write((message[1]))
        

    file.close()
    outFile.close()


if __name__ == "__main__":

    # check if command is in right format
    if len(sys.argv) != 3:
        print("\nPlease run in the format: python(3) [.\\GPT\\scripts\\DataParser.py] [infile.json] [outfile.txt]\n")
        exit()
    
    # check if the infile exists
    if not os.path.exists(sys.argv[1]):
        print("\nInput file does not exist")
        exit()

    parse_data(sys.argv[1], sys.argv[2])