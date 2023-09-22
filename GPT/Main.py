print("Hello World")
# Help me
import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")
# 198 is a newline token

outFile = open("GPT/data/tokens.txt", 'w', encoding='utf-16')
tokens = [i for i in range(1, 100256)]

encoder = tiktoken.get_encoding("cl100k_base")
for token in tokens:
    outFile.write(str(token) + " " + encoder.decode([token]) + "\n")
    