import re

txt = input()

result = re.compile("^\d+$")

if result.fullmatch(txt):
    print("Match")
else:
    print("No match")