"""Building script for the model

Uses PyTorch to build a generative model based on the given dataset text file. 
"""

import torch
import torch.nn as nn
from torch.nn import functional as F
from Model import GPTLanguageModel
from Model import block_size, batch_size, device
from datetime import datetime
from lightning import Fabric
import matplotlib.pyplot as plt
import tiktoken
import time
from pymongo import MongoClient
import certifi
import gridfs
import os
import sys
from dotenv import find_dotenv, load_dotenv


def build(datasetfileName, modelName, showPlot=False):
    start = time.time()

    precision = "bf16-true" if torch.cuda.is_bf16_supported() else "16-mixed"

    # set up fabric
    fabric = Fabric(accelerator="cuda", precision=precision)
    fabric.launch()

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

    # loss function
    @torch.no_grad()
    def estimate_loss():
        out = {}
        model.eval()    # set status to evaluating
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
    with open("GPT/data/" + datasetfileName, "r", encoding='utf-8') as f:
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

    model, optimizer = fabric.setup(model, optimizer)

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
        fabric.backward(loss)
        optimizer.step()        
        
    # evaluate time to run
    end = time.time()
    print(end - start)

    # plot graph
    if showPlot:
        plt.plot(train_losses)
        plt.plot(val_losses)
        plt.title('Loss Graph')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.show()

    # SAVE MODEL
    PATH = "GPT/model/" + modelName + ".pt"
    torch.save(model.state_dict(), PATH)

if __name__ == "__main__":

    # check if command is in right format
    if len(sys.argv) < 3:
        print("\nPlease run in the format: python(3) [.\\GPT\\scripts\\BuildModel.py] [datasetfileName.txt] [ModelName]\n")
        exit()
    
    # check if the dataset exists
    if not os.path.exists("GPT/data/" + sys.argv[1]):
        print("\nDataset does not exist")
        exit()

    build(sys.argv[1], sys.argv[2], showPlot= "-p" in sys.argv)