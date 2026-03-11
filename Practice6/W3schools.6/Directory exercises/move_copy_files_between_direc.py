import shutil
import os

with open("notes.txt", "w") as f:
    f.write("Hello Python directory practice")

shutil.copy("notes.txt", "project/data/notes_copy.txt")
shutil.move("notes.txt", "project/data/notes_moved.txt")

print("Copy and move completed")