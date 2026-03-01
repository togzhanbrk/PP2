import re
s = "one,two;three  four"
print(re.split(r"[,;\s]+", s))