import os

os.makedirs("project/data/raw")  # created multiple folders at once

print("Nested directories created.")

os.makedirs("project/data/raw", exist_ok = True)  #if they already exist we can add like that