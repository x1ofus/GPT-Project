""" Gets dataset file and adds new entries to the master file

Uses DiscordMate browser plugin to get metadata from browser version of discord
Give file path of the textfile as an argument to add new data the the master logs
"""
import json
import sys
import os

def update_dataset(infileName, outfileName):
    
    # load the master file
    masterFile = open("GPT/data/" + outfileName, encoding='utf-8')
    masterDataLog = json.load(masterFile)

    # load the new file
    newLogsText = ""
    with open("GPT/data/" + infileName, "r", encoding='utf-8') as f:
        newLogsText = f.read()
    newDataLog = json.loads(newLogsText)

    # create a mapping for the new userIDs and indexes with the master values
    newIDToMasterID = {}
    
    # look at all users in the new logs
    for newUserIndex, newUserID in enumerate(newDataLog["meta"]["userindex"]):
        if newUserID not in masterDataLog["meta"]["users"]: # if new user
            # add the user to the user index list
            newDataLog["meta"]["userindex"].append(newUserID)
            # add the user to the master user list
            masterDataLog["meta"]["users"][newUserID] = newDataLog["meta"]["users"][newUserID]
        
        # set the mapping from the new index to the master index
        masterUserIndex = newDataLog["meta"]["userindex"].index(newUserID)
        newIDToMasterID[newUserIndex] = masterUserIndex

    # read through each channel in the new logs
    for channelID in list(newDataLog["meta"]["channels"].keys()):

        if channelID not in masterDataLog["meta"]["channels"]:
            newServerNum = len(masterDataLog["meta"]["servers"])    # assign a new server number
        
            # add the new channel the master logs
            masterDataLog["meta"]["servers"].append(newDataLog["meta"]["servers"][newDataLog["meta"]["channels"][channelID]["server"]])
            newDataLog["meta"]["channels"][channelID]["server"] = newServerNum     # set new server number
            masterDataLog["meta"]["channels"][channelID] = newDataLog["meta"]["channels"][channelID]     # add to server list
            masterDataLog["data"][channelID] = {}       # add the new channel
            
        # read through each message in the new logs
        for messageID, data in newDataLog["data"][channelID].items():
            
            if messageID not in masterDataLog["data"][channelID]:
                print("adding: ", messageID, data)
                data["u"] = newIDToMasterID[data["u"]]                  # remap the userIDs
                masterDataLog["data"][channelID][messageID] = data      # add the new log to the data
                
    # dump onto the json file
    with open("GPT/data/" + outfileName, 'w', encoding='utf-8') as f:
        json.dump(masterDataLog, f, ensure_ascii=False, indent=2)

    print("Updated dataset successfully")



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(sys.argv)
        print("\nPlease run in the format: python(3) [.\\GPT\\scripts\\UpdateDataset.py] [newfilename.json] [masterfilename.json]\n")
        exit()

    # check if the infile exists
    if not os.path.exists(sys.argv[1]):
        print("\nInput file does not exist")
        exit()
    
    # check if the infile exists
    if not os.path.exists(sys.argv[2]):
        print("\nMaster file does not exist")
        exit()

    update_dataset(sys.argv[1], sys.argv[2])