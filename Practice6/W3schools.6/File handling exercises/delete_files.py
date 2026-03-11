import os


if os.path.exists("sample.txt"):
    os.remove("sample.txt")
else:
    print("This file does not exist")

os.rmdir("sample_copy")  # rmdir --> means remove directory, it is used to delete an empty folder
