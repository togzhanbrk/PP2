import re
s = "aB7 _-Z"
print(re.findall(r"[a-z]", s))
print(re.findall(r"[A-Z]", s))
print(re.findall(r"[0-9]", s))
print(re.findall(r"[^a-zA-Z0-9\s]", s))