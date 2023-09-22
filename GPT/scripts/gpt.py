# NOTE: add tiktoken_ext package after building
# ADD TO PYINSTALLER CALL: pyinstaller --onedir .\GPT\scripts\gpt.py --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --noconfirm

import sys
import subprocess
import os
from inspect import getsourcefile
from os.path import abspath

from BuildModel import build
from ExportModel import export
#sys.path.pop()

if sys.argv[1] == "train":
    build()
    #subprocess.run(["python", "./GPT/scripts/BuildModel.py"])
if sys.argv[1] == "update":
    pass
    #subprocess.run(["python", "./GPT/scripts/UpdateDataset.py", sys.argv[2]])
if sys.argv[1] == "export":
    export()
    #subprocess.run(["python", "./GPT/scripts/ExportModel.py"])