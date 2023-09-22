def access_model():
    
    from Model import GPTLanguageModel
    from Model import device
    import tiktoken
    import torch
    import time
    import random

    from pymongo import MongoClient
    import certifi
    import gridfs

    import os
    from dotenv import find_dotenv, load_dotenv

    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    CONNECTION_STRING = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASS')}@gptdb.wfjvhng.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    db = client['Models']
    fs = gridfs.GridFS(db)

    data = db.fs.files.find_one({'filename':'Model1'})
    print(data)
    my_id = data['_id']
    outputdata = fs.get(my_id).read()
    PATH = "GPT/model/model.pt"
    output = open(PATH, "wb")
    output.write(outputdata)
    output.close()

    # load in model from file
    model = GPTLanguageModel().to(device)
    model.load_state_dict(torch.load(PATH))

        
    # generate from the model
    # model.eval()
    context = torch.zeros((1, 1), dtype=torch.long, device=device)

    # simulate a chat by printing
    for _ in range(100):
        output, context = model.generate_line(context)
        print(output)
        time.sleep(1 + random.randint(0, 100) / 100)
        
    #print(encoder.decode(model.generate(context, max_new_tokens=500)[0].tolist()))
    #open('output.txt', 'w', encoding='utf-8').write(encoder.decode(model.generate(context, max_new_tokens=10000)[0].tolist()))

if __name__ == "__main__":
    access_model()