f = open("sample.txt")
print(f.readline())  #read one line

with open("sample.txt") as f:
    print(f.read())  #print all the text on file

with open("sample.txt") as f:
    print(f.read(5))  #return the 5 first characters of the file

with open("sample.txt") as f:
    for x in f:   #loop through the file line by line
        print(x) 

f.close() 

