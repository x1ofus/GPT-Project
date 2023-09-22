def export():
    from pymongo import MongoClient
    import certifi
    import gridfs
    from dotenv import find_dotenv, load_dotenv
    import os
    import threading
    import time
    import math
    
    PATH = "GPT/model/model.pt"
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    CONNECTION_STRING = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASS')}@gptdb.wfjvhng.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    client.drop_database('Models')
    db = client['Models']

    file_data = open(PATH, "rb")
    data = file_data.read()
    fs = gridfs.GridFS(db)

    class Watcher(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            
        def run(self):
            while True:
                try:
                    time.sleep(1)
                    if fs.exists({'filename': "Model1"}):
                        print(str(math.ceil(os.path.getsize(PATH)/1024/255))+"/"+str(math.ceil(os.path.getsize(PATH)/1024/255))+ " chunks uploaded")
                        break

                    data = db.fs.chunks.find_one({}, sort=[('n', -1)])
                    
                    print(str(data['n'])+"/"+str(math.ceil(os.path.getsize(PATH)/1024/255))+ " chunks uploaded")
                    
                except Exception as e:
                    print(e)
                

    watcher = Watcher()
    watcher.start()
    fs.put(data, filename='Model1')

if __name__ == "__main__":
    export()