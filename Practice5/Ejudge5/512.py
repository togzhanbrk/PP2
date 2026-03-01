import re

txt = input()

d = re.findall("[0-9]{2,}", txt)

print(" ".join(d))