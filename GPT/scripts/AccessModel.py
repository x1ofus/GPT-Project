"""Access the model and generate new discord messages

Generates lines using the model and pauses between lines for some time.
"""

from Model import GPTLanguageModel
from Model import device

import torch
import time
import random
import os
import sys

def access_model(modelName):

    # write to model file
    PATH = "GPT/model/" + modelName + ".pt"

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
    

if __name__ == "__main__":
    # check if command is in right format
    if len(sys.argv) != 2:
        print("\nPlease run in the format: python(3) [.\\GPT\\scripts\\AccessModel.py] [ModelName]\n")
        exit()

    # check if the model exists
    if not os.path.exists("GPT/model/" + sys.argv[1] + ".pt"):
        print("\nModel does not exist")
        exit()

    access_model(sys.argv[1])