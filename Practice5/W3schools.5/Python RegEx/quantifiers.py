import re
s = "Code: AAA AAAAA AAAAAAA"
print(re.findall(r"A{3}", s))
print(re.findall(r"A{5,}", s))
print(re.findall(r"A{5,7}", s))