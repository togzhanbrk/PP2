import os

folder = "File handling exercises"

for file in os.listdir(folder):
    if file.endswith(".txt"):
        print(file)