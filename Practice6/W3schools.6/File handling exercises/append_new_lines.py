file = open("sample.txt", "a")

file.write("This is third exercise.\n")
file.write("Appending new data to the file.\n")

file.close()

with open("sample.txt", "a") as f:  # "a" is the append to the end of the file
    f.write("Helloooo")

with open("sample.txt") as f:
    print(f.read())

with open("sample.txt", "w") as f:   # "w" will overwrite any existing content
    f.write("Now the file has more content!")

with open("sample.txt") as f:
    print(f.read())

f = open("sample.txt", "x")   # "x" will create a file, returns an error if the file exists

