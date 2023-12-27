"""Export model to database

Pass in the model name and export the model parameter file to the database. Uses
GridFS to split the file into chunks for export.
"""

from pymongo import MongoClient
import certifi
import gridfs
from dotenv import find_dotenv, load_dotenv
import os
import threading
import time
import math
import sys

def export_model(modelName):
    
    
    # get the path of the model
    PATH = "GPT/model/" + modelName + ".pt"
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    # connect to the MongoDB server
    CONNECTION_STRING = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASS')}@gptdb.wfjvhng.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    client.drop_database('Models')
    db = client['Models']

    # split the model into smaller chunks to send to the database
    file_data = open(PATH, "rb")
    data = file_data.read()
    fs = gridfs.GridFS(db)

    # thread watcher for viewing the progress of the model export
    class Watcher(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            
        def run(self):
            while True:
                try:
                    time.sleep(1)
                    # when the model is complete uploaded, end the thread
                    if fs.exists({'filename': "Model1"}):
                        print(str(math.ceil(os.path.getsize(PATH)/1024/255))+"/"+str(math.ceil(os.path.getsize(PATH)/1024/255))+ " chunks uploaded")
                        break

                    data = db.fs.chunks.find_one({}, sort=[('n', -1)])
                    
                    # print the progress of the upload
                    print(str(data['n'])+"/"+str(math.ceil(os.path.getsize(PATH)/1024/255))+ " chunks uploaded")
                    
                except Exception as e:
                    print(e)
                
    # create a watcher to watch over the export
    watcher = Watcher()
    watcher.start()
    fs.put(data, filename='Model1')

if __name__ == "__main__":
    # check if command is in right format
    if len(sys.argv) != 2:
        print("\nPlease run in the format: python(3) [.\\GPT\\scripts\\ExportModel.py] [ModelName]\n")
        exit()

    # check if the model exists
    if not os.path.exists("GPT/model/" + sys.argv[1] + ".pt"):
        print("\nModel does not exist")
        exit()

    export_model(sys.argv[1])