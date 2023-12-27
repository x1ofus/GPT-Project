"""Import model from database

Loads in model from database
"""

from Model import GPTLanguageModel
from Model import device

from pymongo import MongoClient
import certifi
import gridfs

import os
import sys
from dotenv import find_dotenv, load_dotenv

def import_model(modelName):

    # get environment path of the database
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    CONNECTION_STRING = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASS')}@gptdb.wfjvhng.mongodb.net/?retryWrites=true&w=majority"

    # connect to database
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    db = client['Models']
    fs = gridfs.GridFS(db)
    data = db.fs.files.find_one({'filename':'Model1'})
    my_id = data['_id']

    # read from database
    outputdata = fs.get(my_id).read()

    # write to model file
    PATH = "GPT/model/" + modelName + ".pt"
    output = open(PATH, "wb")
    output.write(outputdata)
    output.close()
    

if __name__ == "__main__":
    # check if command is in right format
    if len(sys.argv) != 2:
        print("\nPlease run in the format: python(3) [.\\GPT\\scripts\\ImportModel.py] [ModelName]\n")
        exit()

    import_model(sys.argv[1])