import re

txt1 = "The rain in Spain"
x = re.findall("[a-m]", txt1)  # []
print(x)

txt2 = "That will be 59 dollars"
x = re.findall("\d", txt2)   # \ used to escape special characters
print(x)

txt3 = "hello planet"
x = re.findall("he..o", txt3)  # . any character
print(x)

txt4 = "hello world"
x = re.findall("^hello", txt4)  # ^ starts with
if x:
    print("Yes the string starts with 'hello'")
else:
    print("No match")

txt5 = "hello planet"
x = re.findall("planet$", txt5)  # $ ends with
if x:
    print("Yes, the string ends with 'planet'")
else:
    print("No match")

txt6 = "hello planet"
x = re.findall("he.*o", txt6)  # * zero or more occurrences
print(x)

txt7 = "hello planet"
x = re.findall("he.+o", txt7)  # + one or more occrrences
print(x) 

txt8 = "hello planet"
x = re.findall("he.?o", txt8)  # ? zero or one occurrences
print(x)

txt9 = "hello planet"
x = re.findall("he.{2}o", txt9)  # {} exactly the specified number of occurrences
print(x)

txt10 = "The rain in Spain falls mainly in the plain!"
x = re.findall("falls|stays", txt10)  # | either or
print(x)
if x:
    print("Yes, there is at least one match!")
else:
    print("No match!")