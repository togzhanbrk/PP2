import re

s = input()

d = re.findall("[0-9]", s)

if d:
    for digit in d:
        print(digit, end=" ")
else:
    print()