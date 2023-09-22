import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
print("path", dotenv_path)


print(os.getenv("USER"))
print(os.getenv("PASS"))
