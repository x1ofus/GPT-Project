def build():
    import torch
    import torch.nn as nn
    from torch.nn import functional as F
    from Model import GPTLanguageModel
    from Model import block_size, batch_size, device
    from datetime import datetime

    #from lightning import Fabric
    import matplotlib.pyplot as plt

    import tiktoken
    import time

    from pymongo import MongoClient
    import certifi
    import gridfs

    import os
    from dotenv import find_dotenv, load_dotenv

    start = time.time()

    precision = "bf16-true" if torch.cuda.is_bf16_supported() else "16-mixed"
    print(precision)
    #precision = "16-mixed"

    # fabric = Fabric(accelerator="cuda", precision=precision)
    # fabric.launch()

    # hyper parameters for training
    learning_rate = 3e-4    # learning rate
    max_iters = 100        # total number of iterations
    eval_iters = 10        # number of iterations when evaluating
    eval_interval = 100     # number of iterations until status output

    # grab a batch from the data set
    def get_batch(split):
        # generate a small batch of data of inputs x and targets y
        data = train_data if split == 'train' else val_data
        ix = torch.randint(len(data) - block_size, (batch_size,))
        x = torch.stack([data[i:i+block_size] for i in ix])
        y = torch.stack([data[i+1:i+block_size+1] for i in ix])
        x, y = x.to(device), y.to(device)
        return x, y

    @torch.no_grad()
    def estimate_loss():
        out = {}
        model.eval()    # set status to evaluating
        # 
        for split in ['train', 'val']:
            losses = torch.zeros(eval_iters)
            for k in range(eval_iters):
                X, Y = get_batch(split)
                logits, loss = model(X, Y)
                #losses[k] = loss.mean().item()
                losses[k] = loss.item()
            out[split] = losses.mean()
        model.train()   # set status to training
        return out

    # get the text from the dataset text file
    with open("GPT/data/dataset-userless.txt", "r", encoding='utf-8') as f:
        text = f.read()

    # create tokens from the text
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)

    # split tokens into training and validation data
    data = torch.tensor(tokens, dtype=torch.long)
    n = int(0.9*len(data))  # first 90% will be train, rest val
    train_data = data[:n]
    val_data = data[n:]

    # create GPT model
    model = GPTLanguageModel()
    model.to(torch.device(device))

    # m = model.to(device)
    # print the number of parameters in the model
    print(sum(p.numel() for p in model.parameters())/1e6, 'M parameters')

    # create a PyTorch optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=4e-6)

    #model, optimizer = fabric.setup(model, optimizer)
    train_losses = []
    val_losses = []
    accuracies = []
    # Iterate and train model
    for iter in range(max_iters):
        # every once in a while evaluate the loss on train and val sets
        if iter > 0 and iter % eval_interval == 0 or iter == max_iters - 1:
            losses = estimate_loss()
            print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
            train_losses.append(losses["train"])
            val_losses.append(losses["val"])

        # sample a batch of data
        xb, yb = get_batch('train')

        # evaluate the loss
        logits, loss = model(xb, yb)
        
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        
        # fabric.backward(loss)
        optimizer.step()        
        
    # evaluate time to run
    end = time.time()
    print(end - start)

    # plot graph
    plt.plot(train_losses)
    plt.plot(val_losses)
    plt.title('Loss Graph')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    #plt.show()

    # SAVE MODEL
    PATH = "GPT/model/model.pt"
    torch.save(model.state_dict(), PATH)

    # dotenv_path = find_dotenv()
    # load_dotenv(dotenv_path)

    # CONNECTION_STRING = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASS')}@gptdb.wfjvhng.mongodb.net/?retryWrites=true&w=majority"
    # client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    # client.drop_database('Models')
    # db = client['Models']

    # file_data = open(PATH, "rb")
    # data = file_data.read()

    # fs = gridfs.GridFS(db)
    # fs.put(data, filename='Model1')

if __name__ == "__main__":
    build()