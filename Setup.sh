#!/bin/bash
echo "Downloading Dependencies..."

pip install numpy
pip install scipy
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
pip install tiktoken
pip install lightning
pip install python-dotenv
pip install pyinstaller
