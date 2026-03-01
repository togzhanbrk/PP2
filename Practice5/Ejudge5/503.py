import re

s = input()
p = input()

x = re.findall(p, s)
count = 0

if x:
    for elem in x:
        count += 1
print(count)