import re

s = input()
p = input()

x = re.search(p, s)

if x:
    print("Yes")
else:
    print("No")