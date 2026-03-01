import re

txt = input()

match = re.search(r"\S+@\S+\.\S+", txt)

if match:
    print(match.group())
else:
    print("No email")