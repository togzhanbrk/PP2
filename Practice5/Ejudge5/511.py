import re

txt = input()

x = re.findall("[A-Z]", txt)
count = 0

for ch in x:
    count += 1
print(count)
