import re

txt = input()

if re.search(r"^[a-zA-Z]+[0-9]$", txt):
    print("Yes")
else:
    print("No")
